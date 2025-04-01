import { GoogleGenerativeAI } from "@google/generative-ai";

const googlegenerativeai = new GoogleGenerativeAI(
  import.meta.env.VITE_GOOGLE_AI_API_KEY
);

export class Assistant {
  #chat;
  constructor(model = "gemini-1.5-flash") {
    const gemini = googlegenerativeai.getGenerativeModel({ model });
    this.#chat = gemini.startChat({ history: [] });
  }

  async chat(content) {
    const result = await this.#chat.sendMessage(content);
    return result.response.text();
  }

  async *chatStream(content) {
    const result = await this.#chat.sendMessageStream(content);

    for await (const chunk of result.stream) {
      yield chunk.text();
    }
  }
}
