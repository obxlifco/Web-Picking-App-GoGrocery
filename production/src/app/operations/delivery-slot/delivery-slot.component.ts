import { Component, OnInit } from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';
import { Global } from '../../global/service/global';
import { Time } from '@angular/common';
import {CookieService} from 'ngx-cookie';
import { Http, Response, Headers, RequestOptions} from '@angular/http';
import {throwError as observableThrowError,  Observable } from 'rxjs';
import {catchError, map} from 'rxjs/operators';
import { Router, ActivatedRoute } from '@angular/router';
import { element } from '@angular/core/src/render3';
import { forEach } from '@angular/router/src/utils/collection';
import { DialogsService } from '../../global/dialog/confirm-dialog.service';
@Component({
  selector: 'app-delivery-slot',
  templateUrl: 'templates/delivery-slot.component.html',
})
export class DeliverySlotComponent implements OnInit {
    table: string;heading: string;tablink: string;tabparrentid: any;screen: any;ispopup: any;
    public errorMsg: string;
    public successMsg: string;
    private sub: any;
    public zoneList: any = [];
    public zone_id
    public tabIndex: number;
    public parentId: number = 0;
    public formModel: any = {};
    public userId: any;
    list_data: any = [];
    zone_list: any = [];
    page: any;
    childData = {};
    post_data = {};
    data:any;
    sunday:any=[];monday:any=[];tuesday:any=[];wednesday:any=[];;thursday:any=[];friday:any=[];saturday:any=[];
    public warehouse_list:any=[];
    constructor(
        public _globalService: GlobalService,
        private global: Global,
        private _cookieService: CookieService,
        private globalService: GlobalService,
        private _http: Http,
        private _route: ActivatedRoute,
        private _router: Router,
        private dialogsService: DialogsService,
    ) {
        this.tabIndex = +_globalService.getCookie('active_tabs');
        this.parentId = _globalService.getParentId(this.tabIndex);
    }
    ngOnInit() {
        let userData = this._cookieService.getObject('userData');
        this.userId = userData['uid'];
        // this.loadZoneMaster();
        this.loadWarehouse();
        this.load_del_slot();
    }
    
    load_del_slot(){
        this.global.getWebServiceData('delivery_slot_list','GET','','')
        .subscribe(res=>{
            let data=res.api_status;
            this.sunday=data[0].sunday;
            this.monday=data[1].monday;
            this.tuesday=data[2].tuesday;
            this.wednesday=data[3].wednesday;
            this.thursday=data[4].thursday;
            this.friday=data[5].friday;
            this.saturday=data[6].saturday;
        })

        this.sunday.forEach(day => {
            if(day.warehouse_ids!='') {
                let ids=day.warehouse_ids.toString();
                let array = ids.split(",").map(Number);
                day.warehouse_ids = array;
                // day.warehouse_ids=day.warehouse_ids.toString();
                // day.warehouse_ids = day.warehouse_ids.split(',').map(function(item) {
                //     return parseInt(item, 10);
                // });
            } else {
                day.warehouse_ids = [];
            }
        });
        this.monday.forEach(day => {
            if(day.warehouse_ids!='') {
                let ids=day.warehouse_ids.toString();
                let array = ids.split(",").map(Number);
                day.warehouse_ids = array;
                // day.warehouse_ids=day.warehouse_ids.toString();
                // day.warehouse_ids = day.warehouse_ids.split(',').map(function(item) {
                //     return parseInt(item, 10);
                // });
            } else {
                day.warehouse_ids = [];
            }
        });
        this.tuesday.forEach(day => {
            if(day.warehouse_ids!='') {
                let ids=day.warehouse_ids.toString();
                let array = ids.split(",").map(Number);
                day.warehouse_ids = array;
                // day.warehouse_ids=day.warehouse_ids.toString();
                // day.warehouse_ids = day.warehouse_ids.split(',').map(function(item) {
                //     return parseInt(item, 10);
                // });
            } else {
                day.warehouse_ids = [];
            }
        });
        this.wednesday.forEach(day => {
            if(day.warehouse_ids!='') {
                let ids=day.warehouse_ids.toString();
                let array = ids.split(",").map(Number);
                day.warehouse_ids = array;
                // day.warehouse_ids=day.warehouse_ids.toString();
                // day.warehouse_ids = day.warehouse_ids.split(',').map(function(item) {
                //     return parseInt(item, 10);
                // });
            } else {
                day.warehouse_ids = [];
            }
        });
        this.thursday.forEach(day => {
            if(day.warehouse_ids!='') {
                let ids=day.warehouse_ids.toString();
                let array = ids.split(",").map(Number);
                day.warehouse_ids = array;
                // day.warehouse_ids=day.warehouse_ids.toString();
                // day.warehouse_ids = day.warehouse_ids.split(',').map(function(item) {
                //     return parseInt(item, 10);
                // });
            } else {
                day.warehouse_ids = [];
            }
        });
        this.friday.forEach(day => {
            if(day.warehouse_ids!='') {
                let ids=day.warehouse_ids.toString();
                let array = ids.split(",").map(Number);
                day.warehouse_ids = array;
                // day.warehouse_ids=day.warehouse_ids.toString();
                // day.warehouse_ids = day.warehouse_ids.split(',').map(function(item) {
                //     return parseInt(item, 10);
                // });
            } else {
                day.warehouse_ids = [];
            }
        });
        this.saturday.forEach(day => {
            if(day.warehouse_ids!='') {
                let ids=day.warehouse_ids.toString();
                let array = ids.split(",").map(Number);
                day.warehouse_ids = array;
                // day.warehouse_ids=day.warehouse_ids.toString();
                // day.warehouse_ids = day.warehouse_ids.split(',').map(function(item) {
                //     return parseInt(item, 10);
                // });
            } else {
                day.warehouse_ids = [];
            }
        });
    }
    saveDeliveryTimeSlot(form: any) {
        let data:any={};
        this.sunday.forEach( (day,i) => {
            if(day.is_checked==true){
                day.is_checked=1;
            }else{
                day.is_checked=0;
            }
        })
        this.monday.forEach( (day,i) => {
            if(day.is_checked==true){
                day.is_checked=1;
            }else{
                day.is_checked=0;
            }
        })
        this.tuesday.forEach( (day,i) => {
            if(day.is_checked==true){
                day.is_checked=1;
            }else{
                day.is_checked=0;
            }
        })
        this.wednesday.forEach( (day,i) => {
            if(day.is_checked==true){
                day.is_checked=1;
            }else{
                day.is_checked=0;
            }
        })
        this.thursday.forEach( (day,i) => {
            if(day.is_checked==true){
                day.is_checked=1;
            }else{
                day.is_checked=0;
            }
        })
        this.friday.forEach( (day,i) => {
            if(day.is_checked==true){
                day.is_checked=1;
            }else{
                day.is_checked=0;
            }
        })
        this.saturday.forEach( (day,i) => {
            if(day.is_checked==true){
                day.is_checked=1;
            }else{
                day.is_checked=0;
            }
        })
        data.sunday=this.sunday;
        data.monday=this.monday;
        data.tuesday=this.tuesday;
        data.wednesday=this.wednesday;
        data.thursday=this.thursday;
        data.friday=this.friday;
        data.saturday=this.saturday;
        this.global.getWebServiceData('delivery_slot_update','POST',data,'').subscribe(res => {  
            if (res['status'] == '1') { // success response 
                this._globalService.showToast(res['Message']);
                //this.getAllDeliverySlot();
                this.load_del_slot();

                this._router.navigate(['/delivery_slot/']);
            } else {    
                this._globalService.showToast(res['Message']);
            }
            setTimeout(() => {
                this._globalService.showLoaderSpinner(false);
            });
        }, err => {

        })
    }
    
    add_more(index, day:number) {
        let slot = {
            "is_checked":1,
            "no_of_order":0,
            "start_time":'00:00',
            "end_time":'00:00',
            "cutoff_time":'00:00',
            "based_on":'sameday',
            "warehouse_ids":[]
        }
        if(day==1) {
            this.sunday.push(slot);
        } else if(day==2) {
            this.monday.push(slot);
        } else if(day==3) {
            this.tuesday.push(slot);
        } else if(day==4) {
            this.wednesday.push(slot);
        } else if(day==5) {
            this.thursday.push(slot);
        } else if(day==6) {
            this.friday.push(slot);
        } else if(day==7) {
            this.saturday.push(slot);
        }
    }

    remove(day:number, index) {
        //if(index!=0){
            if(day==1) {
                this.sunday.splice(index, 1);
            } else if(day==2){
                this.monday.splice(index, 1);
            } else if(day==3){
                this.tuesday.splice(index, 1);
            } else if(day==4){
                this.wednesday.splice(index, 1);
            } else if(day==5){
                this.thursday.splice(index, 1);
            } else if(day==6){
                this.friday.splice(index, 1);
            } else if(day==7){
                this.saturday.splice(index, 1);
            }
        //}else{
           // this._globalService.showToast('Parent slot can\'t be remove');
        //}
    }

    deleteSlot(zone_id,start_time,end_time) {
        let msg = '';
        let perm = '';
        let msgp = '';
        msg='Do you really want to delete selected records?';
        msgp='You have no permission to delete!';
        let data:any={};
        data.zone_id = zone_id;
        data.start_time = start_time;
        data.end_time = end_time;
        this.dialogsService.confirm('Warning', msg).subscribe(res => {
            if(res){
                this.global.getWebServiceData('delivery_slot_delete','POST',data,'').subscribe(res => {  
                    if (res['status'] == '1') { // success response 
                        this._globalService.showToast(res['Message']);
                        this.getAllDeliverySlot();
                        this._router.navigate(['/delivery_slot/']);
                    } else {
                        this._globalService.showToast(res['Message']);
                    }
                    setTimeout(() => {
                        this._globalService.showLoaderSpinner(false);
                    });
                }, err => {

                })
            }
        });
    }

    loadZoneMaster() {
        this.global.getWebServiceData('zone_list', 'GET', '', '').subscribe(res => {
            if (res.status == 1) {
                this.zoneList = res.data;
            }
        }, err => console.log(err), function() {});
    }
    loadWarehouse() {
        let websiteId = this._globalService.getWebsiteId();
        this.global.getWebServiceData('warehousestockmanagement/'+websiteId, 'GET', '', '').subscribe(res => {
            if (res.warehouse.length > 0) {
                this.warehouse_list = res.warehouse;
            }
        }, err => console.log(err), function() {});
    }
    getZoneName(zone_id:any){
        this.zoneList.forEach( data => {
            if(data.id==zone_id){
                let name= data.name;
                return name;
            } else {
                return false;
            }
        })
    }

    getAllDeliverySlot() {
        this.post_data = {
            "model": 'EngageboostDeliverySlot',
            "screen_name": 'list',
            "userid": this.userId,
            "website_id": this.globalService.getWebsiteId()
        }

       this.global.getWebServiceData('global_list', 'POST', this.post_data, '').subscribe(res => {
           if(res["status"] == 1) {
               this.sunday = res.sunday;
               this.monday = res.monday;
               this.tuesday = res.tuesday;
               this.wednesday = res.wednesday;
               this.thursday = res.thursday;
               this.friday = res.friday;
               this.saturday = res.saturday;
            } else {
                this._globalService.showToast(res["message"]);
            }
       }, err => {
           this._globalService.showToast("Something went wrong . please try later.");
       })
    }
}