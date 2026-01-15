import fs from 'fs';
import path from 'path';

export class FileHandler {
    private filePath: string;

    constructor(fileName: string) {
        this.filePath = path.join(__dirname, '../../data', fileName);
    }

    public readFile(): Promise<any> {
        return new Promise((resolve, reject) => {
            fs.readFile(this.filePath, 'utf8', (err, data) => {
                if (err) {
                    return reject(err);
                }
                try {
                    const jsonData = JSON.parse(data);
                    resolve(jsonData);
                } catch (parseError) {
                    reject(parseError);
                }
            });
        });
    }

    public writeFile(data: any): Promise<void> {
        return new Promise((resolve, reject) => {
            fs.writeFile(this.filePath, JSON.stringify(data, null, 2), 'utf8', (err) => {
                if (err) {
                    return reject(err);
                }
                resolve();
            });
        });
    }
}