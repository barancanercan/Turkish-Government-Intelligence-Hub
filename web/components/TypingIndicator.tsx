export function TypingIndicator() {
  return (
    <div className="flex gap-1 items-center">
      <div className="flex gap-1">
        <span
          className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"
          style={{ animationDelay: "0ms" }}
        />
        <span
          className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"
          style={{ animationDelay: "150ms" }}
        />
        <span
          className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"
          style={{ animationDelay: "300ms" }}
        />
      </div>
      <span className="text-gray-400 text-sm ml-1">Cevap yazılıyor...</span>
    </div>
  );
}
