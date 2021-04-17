import "./App.css";
import axios from "axios";
import { useState, useEffect } from "react";
import MyTable from "./components/table";
import MyDropzone from "./components/dropzone";

interface Filex {
  filename: string;
  directory: string;
  md5: string;
  version: number;
  message: string;
  uploader: string;
}

async function getFileList() {
  const response = await axios.get<Filex[]>("http://127.0.0.1:8000/list/");
  const { data } = response;
  return data;
}

function App() {
  const [token, setToken] = useState<Filex[]>([]);
  const [increment, setIncrement] = useState(0);
  useEffect(() => {
    async function getToken() {
      setToken(await getFileList());
    }
    getToken();
  }, [increment]);

  async function handleClick() {
    try {
      const y = await fetch("http://localhost:8000/reset/", {
        method: "GET",
      });
      const response = await y;
      if (response.status === 200) {
        setIncrement(increment + 1);
      }
    } catch (error) {
      console.log(error);
    }
  }

  function onDropHandler(acceptedFiles: File[]) {
    acceptedFiles.map(async (file) => {
      const myForm: FormData = new FormData();
      myForm.append("files", file, file.name);
      const x = axios.post("http://localhost:8000/uploadfiles/", myForm, {
        headers: {
          "Content-Type": "multipart/form-data",
          "Access-Control-Allow-Origin": "*",
        },
      });
      if ((await x).status === 200) {
        console.log("success");
        setIncrement(increment + 1);
      } else {
        console.log(x);
        console.log("ERROR GAN!!!");
      }
    });
  }

  return (
    <div>
      <h1>{increment}</h1>
      <MyDropzone onDrop={onDropHandler} />
      <button onClick={handleClick}>Reset</button>
      <MyTable files={token} />
    </div>
  );
}

export default App;
