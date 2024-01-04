import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { DhtComponent } from './dht/dht.component';
import { HomeComponent } from './home/home.component';
import { MaterialModule } from 'src/infrastructure/material/material.module';
import { RgbComponent } from './rgb/rgb.component';

@NgModule({
  declarations: [
    AppComponent,
    DhtComponent,
    HomeComponent,
    RgbComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MaterialModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
