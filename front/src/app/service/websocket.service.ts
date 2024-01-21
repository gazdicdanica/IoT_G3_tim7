import { Injectable } from '@angular/core';
import { io, Socket } from 'socket.io-client';


@Injectable({
  providedIn: 'root'
})
export class WebsocketService {

  private socket: Socket;

  constructor() {
    this.socket = io('http://localhost:5000'); // Connect to Flask-SocketIO server
  }

  getSocket() {
    return this.socket;
  }

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      this.socket.on('connect', () => {
        console.log('Connected to WebSocket');
        resolve();
      });

      this.socket.on('error', (error: any) => {
        console.error('Error connecting to WebSocket:', error);
        reject(error);
      });
    });
  }

  subscribeWakeUpTopic(callback: (message: any) => void): void {
    this.socket.on('wake_up', (message: any) => {
      console.log('Received message:', message);
      callback(message);
    });
  }


  subscribeClockTopic(callback: (message: any) => void) {
    return this.socket.on('time', (message: any) => {
      console.log('Received message:', message);
      callback(JSON.parse(message));
    });
  }

  disconnect(): void {
    if (this.socket && this.socket.connected) {
      this.socket.disconnect();
    }
  }
  // disconnect() {
  //   if (this.stompClient !== null) {
  //     this.stompClient.disconnect();
  //   }
  // }
  
  // closeConnection(stomp : any){
  //   try{
  //     stomp.disconnect();
  //   }catch(e){
  //     return;
  //   }
    
    
  // }
}
