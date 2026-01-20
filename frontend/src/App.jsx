import { useState } from "react";
import AidBot from "./components/AidBot";
import Documents from "./components/Documents";
import Status from "./components/Status";

export default function App() {
  const [view, setView] = useState("chat");

  return (
    <>
      {view === "chat" && <AidBot setView={setView} />}
      {view === "documents" && <Documents setView={setView} />}
      {view === "status" && <Status setView={setView} />}
    </>
  );
}
