import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-frame',
  templateUrl: './frame.component.html',
  styleUrls: ['./frame.component.css']
})
export class FrameComponent {
  id: number = 0;

  url: string = "http://localhost:3000/d-solo/e5980d3e-30ee-4852-bf7b-9cedf4a39956/iot?orgId=1&theme=light&panelId="

  constructor(@Inject(MAT_DIALOG_DATA) data: any){
    this.id = data.id;
    this.url += this.id;
  }

}
