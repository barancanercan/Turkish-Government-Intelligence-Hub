import { NextRequest } from "next/server";

export async function POST(req: NextRequest) {
  const { message } = await req.json();
  const backendUrl = process.env.BACKEND_URL || "http://localhost:8000";

  console.log('[Stream API] Received message:', message);
  console.log('[Stream API] Backend URL:', backendUrl);

  const encoder = new TextEncoder();

  // 10 dakika timeout (büyük modeller için)
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 600000);

  const stream = new ReadableStream({
    async start(streamController) {
      try {
        const requestBody = { question: message, stream: true };
        console.log('[Stream API] Sending to backend:', JSON.stringify(requestBody));

        const response = await fetch(`${backendUrl}/api/v1/query/stream`, {
          method: "POST",
          headers: { 
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
          },
          body: JSON.stringify(requestBody),
          signal: controller.signal,
        });

        console.log('[Stream API] Backend response status:', response.status);
        clearTimeout(timeoutId);

        if (!response.ok || !response.body) {
          const errorText = await response.text();
          console.error('[Stream API] Backend error response:', errorText);
          streamController.enqueue(encoder.encode(`data: ${JSON.stringify({ error: `Backend error: ${response.status} - ${errorText}` })}\n\n`));
          streamController.close();
          return;
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          // Backend zaten SSE formatında gönderiyor, doğrudan pass-through
          const chunk = decoder.decode(value);
          streamController.enqueue(encoder.encode(chunk));
        }

        streamController.close();
      } catch (error) {
        clearTimeout(timeoutId);
        const errorMessage = error instanceof Error ? error.message : "Stream error";
        streamController.enqueue(encoder.encode(`data: ${JSON.stringify({ error: errorMessage })}\n\n`));
        streamController.close();
      }
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      "Connection": "keep-alive",
    },
  });
}
