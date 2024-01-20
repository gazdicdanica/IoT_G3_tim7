import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environment/environment';

@Injectable({
  providedIn: 'root'
})
export class ServiceService {

  constructor(private http: HttpClient) { }

  setWakeUpTime(time: any){
    return this.http.get(environment.apiHost + 'api/set_wakeup_time?time='+time);
  }

  turnOffWakeUp(){
    return this.http.get(environment.apiHost + 'api/turn_off_alarm');
  }

  change_rgb_color(color: any){
    return this.http.put(environment.apiHost + '/api/change_rgb', {"color": color});
  }
}
