import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const { message } = await req.json();

    if (!message) {
      return NextResponse.json({ error: "Mesaj gerekli" }, { status: 400 });
    }

    // Call Python backend (FastAPI)
    const backendUrl = process.env.BACKEND_URL || "http://localhost:8000";

    // Try without auth for demo
    const response = await fetch(`${backendUrl}/api/v1/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        question: message,
        top_k: 5,
        stream: false
      }),
    });

    if (!response.ok) {
      // If auth required, return demo response
      return NextResponse.json({
        response: "API bağlantısı için lütfen backend'i başlatın: uvicorn src.api.main:app --reload",
        sources: [],
        queryType: "error",
        qualityScore: 0,
      });
    }

    const data = await response.json();

    return NextResponse.json({
      response: data.answer || data.response || "Yanıt alınamadı",
      sources: data.sources || [],
      queryType: data.query_type,
      qualityScore: data.latency_ms ? 0.8 : 0,
    });
  } catch (error) {
    console.error("Error:", error);
    return NextResponse.json(
      { 
        response: "Backend'e bağlanılamadı. Lütfen backend'i başlatın.",
        error: "Bağlantı hatası" 
      },
      { status: 200 }
    );
  }
}
