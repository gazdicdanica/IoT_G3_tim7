import { Component } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { RgbComponent } from '../rgb/rgb.component';
import { ClockComponent } from '../clock/clock.component';
import { WakeUpComponent } from '../wake-up/wake-up.component';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {

  constructor(private dialog: MatDialog){}

  dialogConfig = new MatDialogConfig();
  
  ngOnInit(): void {
    this.dialogConfig.disableClose = false;
    this.dialogConfig.autoFocus = true;
    this.dialogConfig.closeOnNavigation = true;
    this.dialogConfig.width = '30%';
    this.dialogConfig.height = 'auto';
  }

  openClockDialog(){
    this.dialog.open(ClockComponent, this.dialogConfig);

  }

  openRGBDialog(){
    this.dialog.open(RgbComponent, this.dialogConfig);

  }

  wakeUp(){
    this.dialog.open(WakeUpComponent, this.dialogConfig);
  }

}
