import { Component } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { RgbComponent } from '../rgb/rgb.component';
import { ClockComponent } from '../clock/clock.component';
import { WakeUpComponent } from '../wake-up/wake-up.component';
import { WebsocketService } from '../service/websocket.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {

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

}
