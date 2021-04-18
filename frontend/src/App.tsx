import "./App.css";
import axios from "axios";
import { useState, useEffect } from "react";
import MyTable from "./components/table";
import MyDropzone from "./components/dropzone";
import { checksum } from "./function/checksum";

interface Filex {
  filename: string;
  directory: string;
  md5: string;
  version: number;
  message: string;
  uploader: string;
}

async function getFileList() {
  const response = await axios.get<Filex[]>("/list/");
  const { data } = response;
  return data;
}

function App() {
  const [token, setToken] = useState<Filex[]>([]);
  const [increment, setIncrement] = useState(false);

  function handleToggle() {
    setIncrement(increment ? false : true)
    console.log("toggling");
  }
  useEffect(() => {
    async function getToken() {
      setToken(await getFileList());
    }
    getToken();
  }, [increment]);

  async function handleClick() {
    try {
      const y = await fetch("/reset/", {
        method: "GET",
      });
      const response = await y;
      if (response.status === 200) {
        handleToggle();
      }
    } catch (error) {
      console.log(error);
    }
  }

  function delay(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }


  async function onDropHandler(acceptedFiles: File[]) {
    const asyncres = await Promise.all(acceptedFiles.map(async (file) => {
      const myForm: FormData = new FormData();
      const filemd5: any = await checksum(file);
      myForm.append("file", file, file.name);
      myForm.append("filemd5", filemd5);
      // const bl = file.slice(0, 10)
      // const tx = await bl.text()
      // console.log(tx)
      // myForm.forEach((value, key) => {
      //   console.log(key + " " + value)
      // });
      try {
        const x = await axios.post("/uploadfiles/", myForm, {
          headers: {
            "Content-Type": "multipart/form-data",
            "Access-Control-Allow-Origin": "*",
          },
        });
        if (x.status === 200) {
          //await delay(10000);
          return x
        }
      } catch (error) {
        console.log(error);
        console.log('error uploading: ' + file.name)
        const arr = []
        arr.push(file)
        onDropHandler(arr)
        return error
      } finally {
        handleToggle();
      }
    }));
    console.log(asyncres);
  }

  return (
    <div>
      <h1>{increment ? "true" : "false"} ntabas</h1>
      <MyDropzone onDrop={onDropHandler} />
      <button onClick={handleClick}>Reset</button>
      <MyTable files={token} />
    </div>
  );
}

export default App;
