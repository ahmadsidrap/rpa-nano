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
      try {
        const response = await fetch(process.env.NEXT_PUBLIC_API_URL + "/rpa/container");
        const result = await response.json();
        setData(result.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }

    fetchData();
  }, []);

  return (
    <div className="col-span-12 row-auto rounded-xl bg-muted p-4">
      <h2>Containers</h2>
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
