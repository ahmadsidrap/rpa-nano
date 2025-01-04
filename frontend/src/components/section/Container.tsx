"use client";

import { useEffect, useState } from "react";

export default function Container() {
  interface ContainerData {
    Names: string;
    CreatedAt: string;
    Status: string;
    State: string;
  }

  const [data, setData] = useState<ContainerData[]>([]);
  
  useEffect(() => {
    async function fetchData() {
      sendCommand("show active containers");
    }

    fetchData();
  }, []);

  async function sendCommand(message: string) {
    try {
      const url = process.env.NEXT_PUBLIC_API_URL + "/api/rpa/nlp";
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
      });
      const result = await response.json();
      setData(result.data);
    } catch (error) {
      console.error("Error sending message:", error);
    }
  }

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.target as HTMLFormElement);
    const message = formData.get("message");
    sendCommand(message as string);
  }

  return (
    <div className="col-span-12 row-auto rounded-xl bg-muted p-4">
      <form onSubmit={handleSubmit}>
        <textarea
          name="message"
          placeholder="Enter message"
          className="border rounded p-2 w-full"
          required
        />
        <div className="flex justify-end mt-2">
          <button type="submit" className="p-2 bg-primary text-white rounded">
            Send
          </button>
        </div>
      </form>
      <div className="flex flex-col gap-4 py-4">
      {data.map((item, i) => (
        <div key={i}>
          <h4 className="text-primary transition-colors duration-150 ease-in group-hover:text-primary/70">
            {item.Names}
          </h4>
          <p className="line-clamp-2 text-sm text-muted-foreground">
            <span><b>State:</b> {item.State}</span>・<span><b>Status:</b> {item.Status}</span>
          </p>
        </div>
      ))}
      </div>
    </div>
  );
}
