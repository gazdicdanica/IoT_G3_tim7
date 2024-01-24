import { Component } from '@angular/core';
import { MatDialog, MatDialogConfig, MatDialogRef } from '@angular/material/dialog';
import { RgbComponent } from '../rgb/rgb.component';
import { ClockComponent } from '../clock/clock.component';
import { WakeUpComponent } from '../wake-up/wake-up.component';
import { WebsocketService } from '../service/websocket.service';
import { AlarmComponent } from '../alarm/alarm.component';
import { FrameComponent } from '../frame/frame.component';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {

  alarmDialog!: MatDialogRef<AlarmComponent>;
  peopleCount: number = 0;

  constructor(private wsService: WebsocketService, private dialog: MatDialog){}

  dialogConfig = new MatDialogConfig();
  
  ngOnInit(): void {
    this.dialogConfig.disableClose = false;
    this.dialogConfig.autoFocus = true;
    this.dialogConfig.closeOnNavigation = true;
    this.dialogConfig.width = '30%';
    this.dialogConfig.height = 'auto';


    this.wsService.connect().then(() => {
      this.wsService.subscribeWakeUpTopic((message: any) => {
        console.log("wake up");
        this.wakeUp();
      });
      
      this.wsService.subscribeAlarmTopic((message: any) => {
        if(message["alarm"] == 1) this.alarm();
        else this.alarmDialog.close();
      });

      this.wsService.subscribePeopleCountTopic((message: any) => {
        this.peopleCount = message["people_count"];
      });
    }).catch((error: any) => {
      console.error('Error connecting to WebSocket:', error);
    });
  
  }

  openClockDialog(){
    this.dialogConfig.width = '35%';
    this.dialog.open(ClockComponent, this.dialogConfig);
    this.dialogConfig.width = '30%';

  }

  openRGBDialog(){
    this.dialog.open(RgbComponent, this.dialogConfig);

  }

  wakeUp(){
    this.dialog.open(WakeUpComponent, this.dialogConfig);
  }

  alarm(){
    this.dialogConfig.width = 'auto';
    this.alarmDialog = this.dialog.open(AlarmComponent, this.dialogConfig);
    this.dialogConfig.width = '30%';
  }

  openFrame(id: number){
    this.dialogConfig.width = 'auto';
    this.dialogConfig.data = {id: id};
    this.dialog.open(FrameComponent, this.dialogConfig);
    this.dialogConfig.width = '30%';
  }
}
