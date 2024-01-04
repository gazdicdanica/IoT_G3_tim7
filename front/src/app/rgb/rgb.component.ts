import { Component } from '@angular/core';

@Component({
  selector: 'app-rgb',
  templateUrl: './rgb.component.html',
  styleUrls: ['./rgb.component.css']
})
export class RgbComponent {
  colors: string[] = ["#FF0000", "#00CC00", "#0000FF", "#FFFF00", "#800080", "#87CEFA", "#FFFAFA"];
  selectedColor: string | null = null;

  ngOnInit(): void {
    // TODO: Get current color
  }

  getChunkedColors(): string[][] {
    const chunkSize = 3;
    const chunkedColors: string[][] = [];

    for (let i = 0; i < this.colors.length; i += chunkSize) {
      chunkedColors.push(this.colors.slice(i, i + chunkSize));
    }

    return chunkedColors;
  }

  isColorSelected(color: string): boolean {
    return this.selectedColor === color;
  }

  selectColor(color: string){
    this.selectedColor = color;
    console.log(color);
  }

  turnOff(){
    this.selectedColor = null;
  }

}
