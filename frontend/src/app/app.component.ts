import { mergeMap, map, filter} from 'rxjs/operators';
import { Component,Inject,OnInit,AfterViewInit,NgZone } from '@angular/core';
import { Router, NavigationEnd, ActivatedRoute } from '@angular/router';
import { Title, DOCUMENT } from '@angular/platform-browser';
import { CookieService } from 'ngx-cookie';
import { Global,GlobalVariable } from './global/service/global';
import { GlobalService } from './global/service/app.global.service';
import {WarehouseService} from './global/service/warehouse.service';
import { DialogsService } from './global/dialog/confirm-dialog.service';
import { SwPush,SwUpdate} from '@angular/service-worker';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import {WarehouselistComponent} from './global/dialog/warehouselist/warehouselist.component';
import {LocationdialogComponent} from './global/dialog/locationdialog/locationdialog.component';
import {FinetuninglocationComponent} from './global/dialog/finetuninglocation/finetuninglocation.component';
import {NowarehousefoundComponent} from './global/dialog/nowarehousefound/nowarehousefound.component';
import { storecategorylistComponent } from './global/dialog/storecategorylist/storecategorylist.component';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: [Global]
})
export class AppComponent implements OnInit {
    public geoip2:any;
    public userGlobalLocation:Object;
    constructor( 
      private swUpdate: SwUpdate,
      public swPush: SwPush,
      private _warehouse:WarehouseService,
      public dialog: MatDialog,
      private _globalService:GlobalService
    ) {
      //this.geoip2.insights(success => this.onGeoApiSucess(location))
    }
    /**
     * Callback method for getting geoapi data
     * @access public
    */
    onGeoApiSucess(location) {
      // console.log("**************** Fetched location data ***************");
      // console.log(location);
    }
    // Initialization method
    ngOnInit() {
      //this.userGlobalLocation = this._globalService.getCookie('current_user_location') != '' ? JSON.parse(this._globalService.getCookie('current_user_location')) : {};
      if (this.swUpdate.isEnabled) {
        this.swUpdate.available.subscribe((evt) => {
            // console.log('service worker updated');
        });
        this.swUpdate.checkForUpdate().then(() => {
            // noop
        }).catch((err) => {
            console.error('error when checking for update', err);
        });
      }
   }

  ngAfterViewInit(){
   
  }  

  updateSubscribe(email:string,campaign_id:number,website_id:number) {
   
  }

  updateUserClick(email:string,campaign_id:number,website_id:number){
    
  }
}