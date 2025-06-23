import { LangChainAdapter } from "ai";
import { NextResponse } from "next/server";
import { A2AClient, Message } from "@a2a-js/sdk";
import crypto from "node:crypto";

interface SlidesRequest {
  title: string; // Presentation title
  outline: string[]; // Array of main topics with markdown content
  language: string; // Language to use for the slides
  tone: string; // Style for image queries (optional)
}

function generateId() {
  return crypto.randomUUID();
}

const A2A_AGENT_SERVER_URL = process.env.A2A_AGENT_SLIDES_URL ?? "http://localhost:10011";

console.log("A2A Agent Slides Server URL:", A2A_AGENT_SERVER_URL);

// Helper function to convert an async string iterator to a ReadableStream
function iteratorToStream(
  iterator: AsyncGenerator<string>,
): ReadableStream<string> {
  return new ReadableStream({
    async pull(controller) {
      const { value, done } = await iterator.next();
      if (done) {
        controller.close();
      } else {
        controller.enqueue(value);
      }
    },
  });
}

async function* generateSlidesStream(
  serverUrl: string,
  slidesRequest: SlidesRequest,
) {
  const client = new A2AClient(serverUrl);

  const messageId = generateId();
  const content = `Please generate a presentation with the following details:
Title: ${slidesRequest.title}
Language: ${slidesRequest.language}
Tone for images: ${slidesRequest.tone}

Outline:
${slidesRequest.outline.map((item, index) => `${index + 1}. ${item}`).join("\n")}
`;

  const message: Message = {
    messageId,
    kind: "message",
    role: "user",
    parts: [{ kind: "text", text: content }],
  };

  try {
    const stream = client.sendMessageStream({ message });
    for await (const event of stream) {
      console.log("Received event:", event);
      if (
        event.kind === "status-update" &&
        event.status &&
        event.status.message
      ) {
        const nestedMessage = event.status.message;
        for (const part of nestedMessage.parts) {
          if (part.kind === "text") {
            console.log(
              "Yielding text part (from status-update message):",
              part.text,
            );
            yield part.text;
          }
        }
      } else if (
        event.kind === "artifact-update" &&
        event.artifact &&
        event.artifact.parts
      ) {
        console.log("Processing artifact-update event.");
        for (const part of event.artifact.parts) {
          if (part.kind === "text") {
            console.log("Yielding text part (from artifact):", part.text);
            // yield part.text;
          }
        }
      } else {
        console.log("Received event (ignoring):", event);
      }
    }
  } catch (error) {
    console.error("Error communicating with A2A client:", error);
    yield `Error: Failed to communicate with agent. ${(error as Error).message}`;
  }
}

export async function POST(req: Request) {
  try {
    const { title, outline, language, tone } =
      (await req.json()) as SlidesRequest;

    if (!title || !outline || !Array.isArray(outline) || !language) {
      return NextResponse.json(
        { error: "Missing required fields" },
        { status: 400 },
      );
    }
    const stream = iteratorToStream(
      generateSlidesStream(A2A_AGENT_SERVER_URL, {
        title,
        outline,
        language,
        tone,
      }),
    );
    return LangChainAdapter.toDataStreamResponse(stream);
  } catch (error) {
    console.error("Error in presentation generation:", error);
    return NextResponse.json(
      { error: "Failed to generate presentation slides" },
      { status: 500 },
    );
  }
}
