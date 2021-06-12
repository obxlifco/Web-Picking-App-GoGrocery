import { Component, OnInit, ViewChild, ElementRef,NgZone,AfterViewInit,Inject} from '@angular/core';
/*import { MapsAPILoader, MouseEvent } from '@agm/core';*/
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import { FormGroup, FormBuilder } from '@angular/forms';

import { } from 'googlemaps';

@Component({
  selector: 'app-finetuninglocation',
  templateUrl: './finetuninglocation.component.html',
  styleUrls: ['./finetuninglocation.component.css']
})
export class FinetuninglocationComponent implements OnInit,AfterViewInit{
    title: string = 'AGM project';
    latitude: number;
    longitude: number;
    zoom: number = 8;
    address: string = '';
    private geoCoder;
    private place;
    @ViewChild('gmap') gmapElement: any;
    map: google.maps.Map;
    constructor(
      public dialogRef: MatDialogRef<FinetuninglocationComponent>,
      @Inject(MAT_DIALOG_DATA) public data,
      /*private mapsAPILoader: MapsAPILoader,*/
      private ngZone: NgZone,

    ) { 
    }
    @ViewChild('search') public searchElementRef: ElementRef;
    autocompleteInput: string;
    queryWait: boolean;

    ngOnInit() {
    if(this.data && Object.keys(this.data).length > 0) {
      this.latitude = this.data['latitude'];
      this.longitude = this.data['longitude'];
    }

    /*this.mapsAPILoader.load().then(() => {
      this.geoCoder = new google.maps.Geocoder;
      this.setCurrentLocation();
      let autocomplete = new google.maps.places.Autocomplete(this.searchElementRef.nativeElement, {
        types: ["address"]
      });
      autocomplete.addListener("place_changed", () => {
        this.ngZone.run(() => {
          //get the place result
          let place: google.maps.places.PlaceResult = autocomplete.getPlace();
          //verify result
          if (place.geometry === undefined || place.geometry === null) {
            return;
          } 
          //set latitude, longitude and zoom
          this.latitude = place.geometry.location.lat();
          this.longitude = place.geometry.location.lng();
          this.zoom = 12;
        });
      });
    });*/
  }

  ngAfterViewInit() {
    this.geoCoder = new google.maps.Geocoder;
      this.setCurrentLocation();
      let autocomplete = new google.maps.places.Autocomplete(this.searchElementRef.nativeElement, {
        //types: ["address"]
      });
      this.mapView();
      autocomplete.addListener("place_changed", () => {
        this.ngZone.run(() => {
          //get the place result
          let place: google.maps.places.PlaceResult = autocomplete.getPlace();
          //verify result
          if (place.geometry === undefined || place.geometry === null) {
            return;
          } 
          //set latitude, longitude and zoom
          this.latitude = place.geometry.location.lat();
          this.longitude = place.geometry.location.lng();
          this.zoom = 8;
          this.mapView();
          this.getAddress(this.latitude,this.longitude); 
        });
      }
      );

  }
 
  // Get Current Location Coordinates
  private setCurrentLocation() {
    if(this.latitude && this.longitude) {
      this.zoom = 8;
      this.getAddress(this.latitude, this.longitude);

    } else {
      navigator.geolocation.getCurrentPosition((position) => {
        this.latitude = position.coords.latitude;
        this.longitude = position.coords.longitude;
        this.zoom = 8;
        this.getAddress(this.latitude, this.longitude);
        this.mapView();
      });
    }
 }
 


 setCurentAddress() {
   console.log("Current address")
  navigator.geolocation.getCurrentPosition((position) => {
    this.latitude = position.coords.latitude;
    this.longitude = position.coords.longitude;
    this.zoom = 8;
    this.getAddress(this.latitude, this.longitude);
    console.log("Current address loading")
    this.mapView();
  });
          
    /*if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition((position) => {
        this.latitude = position.coords.latitude;
        this.longitude = position.coords.longitude;
        this.zoom = 8;
        this.getAddress(this.latitude, this.longitude);
      });
    }*/
  }
  public mapView() {
    let mapProp = {
      center: new google.maps.LatLng(this.latitude,this.longitude),
      zoom: 8,
      mapTypeId: google.maps.MapTypeId.TERRAIN,

    };
    this.map = new google.maps.Map(this.gmapElement.nativeElement,mapProp);
    let latObject:any = {lat:this.latitude, lng:this.longitude };
    var marker = new google.maps.Marker({
      position: latObject,
      map: this.map,
      draggable:true,
      icon :'../../../../assets/images/location-pointer.png'
    });
    marker.addListener('dragend',(event) => {
      this.latitude  = event.latLng.lat();
      this.longitude = event.latLng.lng();
      this.getAddress(this.latitude,this.longitude); 

    })
    this.smoothZoom(this.map,12,this.map.getZoom());
  }


   smoothZoom (map, max, cnt) {
    if (cnt >= max) {
      
        return;
    }
    else {
     // alert("1111");
     let self = this;
        let z = google.maps.event.addListener(map, 'zoom_changed', function(event){
            google.maps.event.removeListener(z);
            self.smoothZoom(map, max, cnt + 1);
        });
        setTimeout(function(){map.setZoom(cnt)}, 80); // 80ms is what I found to work well on my system -- it might not work well on all systems
    }
}  
  /*markerDragEnd($event: MouseEvent) {
    // console.log($event);
    this.latitude = $event.coords.lat;
    this.longitude = $event.coords.lng;
    this.getAddress(this.latitude, this.longitude);
  }*/
 
  getAddress(latitude, longitude) {
    this.geoCoder.geocode({ 'location': { lat: latitude, lng: longitude } }, (results, status) => {
      // console.log(results);
      // console.log(status);
      if (status === 'OK') {
        if (results[0]) {
          this.zoom = 12;
          this.address = results[0].formatted_address;
        } else {
          window.alert('No results found');
        }
      } else {
          window.alert('Geocoder failed due to: ' + status);
      } 
    });
  }
  verifyWareHouseOnSelectedLocation() {
     let locationData = {
      latitude : this.latitude,
      longitude : this.longitude
    }
    this.dialogRef.close(locationData);
  }
  verifyWareHouseClose(){
    this.dialogRef.close();
  }
}
