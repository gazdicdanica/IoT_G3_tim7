import { Component, ViewChild } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { Howl } from 'howler';

@Component({
  selector: 'app-wake-up',
  templateUrl: './wake-up.component.html',
  styleUrls: ['./wake-up.component.css']
})
export class WakeUpComponent {

  constructor(private dialogRef: MatDialogRef<WakeUpComponent>) { }
  
  ngOnInit(){
  }

  close(){
    // TODO: stop the alarm
    this.dialogRef.close();
  }

}
