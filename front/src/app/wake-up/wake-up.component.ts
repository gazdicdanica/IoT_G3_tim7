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

  audio: any;

  ngOnInit(){
    this.audio = new Audio();
    this.audio.src = "../../assets/dire_straits.mp3";
    this.audio.load();
    this.audio.play();
  }

  close(){
    // TODO: stop the alarm
    this.dialogRef.close();
    this.audio.pause();
  }

}
