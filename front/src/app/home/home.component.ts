import { Component } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { RgbComponent } from '../rgb/rgb.component';
import { ClockComponent } from '../clock/clock.component';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {

  constructor(private dialog: MatDialog){}

  ngOnInit(): void {
  }

  openClockDialog(){
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = false;
    dialogConfig.autoFocus = true;
    dialogConfig.closeOnNavigation = true;
    dialogConfig.width = '30%';
    dialogConfig.height = 'auto';

    const dialogRef = this.dialog.open(ClockComponent, dialogConfig);


  }

  openRGBDialog(){
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = false;
    dialogConfig.autoFocus = true;
    dialogConfig.closeOnNavigation = true;
    dialogConfig.width = '30%';
    dialogConfig.height = 'auto';

    const dialogRef = this.dialog.open(RgbComponent, dialogConfig);

  }

}