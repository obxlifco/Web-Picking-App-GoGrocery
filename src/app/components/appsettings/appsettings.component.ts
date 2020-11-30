import { Component, OnInit } from '@angular/core';
import { DatabaseService } from 'src/app/services/database/database.service';

@Component({
  selector: 'app-appsettings',
  templateUrl: './appsettings.component.html',
  styleUrls: ['./appsettings.component.scss']
})
export class AppsettingsComponent implements OnInit {

  timerValue:any
  timerData:any=[
    {
      value:1,
      name: "1 Minutes"
    },
    {
      value:3,
      name: "3 Minutes"
    },
    {
      value:5,
      name: "5 Minutes"
    },
    {
      value:8,
      name: "8 Minutes"
    },
    {
      value:10,
      name: "10 Minutes"
    },
    {
      value:15,
      name: "15 Minutes"
    },
    {
      value:20,
      name: "20 Minutes"
    },
    {
      value:30,
      name: "30 Minutes"
    },
    {
      value:60,
      name: "1 Hour"
    },
  ]
  constructor(public db:DatabaseService) { }

  ngOnInit(): void {
  }

  setTimer(){

  }

  onChange(event:any){
    console.log(event.target.value);
    this.db.setNotificationTime(event.target.value*60000)
    // timer(0, 60000).pipe(
  }
}
