import { Component } from '@angular/core';

@Component({
  selector: 'app-clock',
  templateUrl: './clock.component.html',
  styleUrls: ['./clock.component.css']
})
export class ClockComponent {

  // TODO update currentTime through websockets
  currentTime: Date = new Date();
  alarm: Date | null = null;


  save() {
    console.log('Selected time:', this.alarm);
    // Handle the changed time value here
  }

  reset(){
    this.alarm = null
  }

}
