import "./App.css";
import axios from "axios";
import { useState, useEffect, useMemo } from "react";
import { useTable } from "react-table";

interface File {
  filename: string;
  directory: string;
  md5: string;
  version: number;
  message: string;
  uploader: string;
}

async function getFileList() {
  const response = await axios.get<File[]>("http://127.0.0.1:8000/list/");
  const { data } = response;
  return data;
}

function App() {
  const [token, setToken] = useState<File[]>([]);
  useEffect(() => {
    async function getToken() {
      setToken(await getFileList());
    }
    getToken();
  }, []);

  const data = useMemo<File[]>(() => token, [token]);

  const columns = useMemo<any>(
    () => [
      {
        Header: "File Name",
        accessor: "filename", // accessor is the "key" in the data
      },
      {
        Header: "Directory",
        accessor: "directory",
      },
      {
        Header: "MD5",
        accessor: "md5",
      },
      {
        Header: "Version",
        accessor: "version",
      },
      {
        Header: "Message",
        accessor: "message",
      },
      {
        Header: "Uploader",
        accessor: "uploader",
      },
    ],
    []
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable<File>({ columns, data });

  return (
    <div>
      <table {...getTableProps()}>
        <thead>
          {
            // Loop over the header rows
            headerGroups.map((headerGroup) => (
              // Apply the header row props
              <tr {...headerGroup.getHeaderGroupProps()}>
                {
                  // Loop over the headers in each row
                  headerGroup.headers.map((column) => (
                    // Apply the header cell props
                    <th {...column.getHeaderProps()}>
                      {
                        // Render the header
                        column.render("Header")
                      }
                    </th>
                  ))
                }
              </tr>
            ))
          }
        </thead>
        {/* Apply the table body props */}
        <tbody {...getTableBodyProps()}>
          {
            // Loop over the table rows
            rows.map((row) => {
              // Prepare the row for display
              prepareRow(row);
              return (
                // Apply the row props
                <tr {...row.getRowProps()}>
                  {
                    // Loop over the rows cells
                    row.cells.map((cell) => {
                      // Apply the cell props
                      return (
                        <td {...cell.getCellProps()}>
                          {
                            // Render the cell contents
                            cell.render("Cell")
                          }
                        </td>
                      );
                    })
                  }
                </tr>
              );
            })
          }
        </tbody>
      </table>
    </div>
  );
}

export default App;
