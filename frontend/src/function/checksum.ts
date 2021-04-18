import SparkMD5 from 'spark-md5';

// Read in chunks of 2MB
const CHUCK_SIZE = 2097152;

/**
 * Incrementally calculate checksum of a given file based on MD5 algorithm
 */
export const checksum = (file: File) =>
    new Promise((resolve, reject) => {
        let currentChunk = 0;
        const chunks = Math.ceil(file.size / CHUCK_SIZE);
        const blobSlice = File.prototype.slice
        const spark = new SparkMD5.ArrayBuffer();
        const fileReader = new FileReader();

        const loadNext = () => {
            const start = currentChunk * CHUCK_SIZE;
            const end =
                start + CHUCK_SIZE >= file.size ? file.size : start + CHUCK_SIZE;

            // Selectively read the file and only store part of it in memory.
            // This allows client-side applications to process huge files without the need for huge memory
            fileReader.readAsArrayBuffer(blobSlice.call(file, start, end));
        };

        fileReader.onload = (e: any) => {
            spark.append(e.target.result);
            currentChunk++;

            if (currentChunk < chunks) loadNext();
            else resolve(spark.end());
        };

        fileReader.onerror = () => {
            return reject('Calculating file checksum failed');
        };

        loadNext();
    });