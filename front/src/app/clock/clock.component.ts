import { Component } from '@angular/core';
import { ServiceService } from '../service/service.service';
import { WebsocketService } from '../service/websocket.service';

@Component({
  selector: 'app-clock',
  templateUrl: './clock.component.html',
  styleUrls: ['./clock.component.css']
})
export class ClockComponent {

  constructor(private service: ServiceService, private wsService: WebsocketService){}

  // TODO update currentTime through websockets
  currentTime: Date = new Date();
  alarm: Date | null = null;

  save() {
    console.log('Selected time:', this.alarm);
    this.service.setWakeUpTime(this.alarm).subscribe((data: any) => {
      console.log(data);
    });
    // Handle the changed time value here
  }

  reset(){
    this.alarm = null
  }

}
