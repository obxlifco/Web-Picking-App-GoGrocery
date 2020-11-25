import { Component, Inject, OnInit } from '@angular/core';
import { ViewChild } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

/// <reference types="@types/googlemaps" />
import {} from 'googlemaps';
import { DialogData } from '../addnewproduct/addnewproduct.component';

declare module 'googlemaps';
@Component({
  selector: 'app-mapmodal',
  templateUrl: './mapmodal.component.html',
  styleUrls: ['./mapmodal.component.scss']
})
export class MapmodalComponent implements OnInit {

  @ViewChild('map') mapElement: any;
   map:any= google.maps.Map;
  lat:any="25.346254"
  lng:any="55.420933"
  constructor( public dialogRef: MatDialogRef<MapmodalComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) {
      
      setTimeout(() => {
        this.initmap(data);
      }, 300);
     }

  ngOnInit(): void {
  }

  initmap(data:any){
    console.log("lat long : ",data.data);
    
    const mapProperties = {
      center: new google.maps.LatLng(data.data.lat_val, data.data.long_val),
      zoom: 15,
      mapTypeId: google.maps.MapTypeId.ROADMAP
 };
 this.map = new google.maps.Map(this.mapElement.nativeElement,    mapProperties);
 
 
const marker = new google.maps.Marker({
  position: new google.maps.LatLng(data.data.lat_val, data.data.long_val),
  map: this.map,
  title: 'Deliver Address'
  });
  // this.map = new google.maps.Map(this.mapElement.nativeElement,    marker);
  }

}
