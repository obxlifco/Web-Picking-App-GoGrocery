import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { GroupService } from './employee.group.service';
import { GlobalService } from '../../global/service/app.global.service';
import { Global } from '../../global/service/global';
import { AddEditTransition } from '../.././addedit.animation';

@Component({
    templateUrl: './templates/add_groups.html',
    providers: [GroupService, Global],
    animations: [AddEditTransition],
    host: {
        '[@AddEditTransition]': ''
    },
})
export class GroupAddEditComponent implements OnInit, OnDestroy {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public menu_list: any;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public ipaddress: any;
    public checkAll: boolean;
    public websitelist:any;
    public warehouse_list:any = [];
    constructor(
        private _groupService: GroupService,
        public _globalService: GlobalService,
        private _router: Router,
        private _route: ActivatedRoute,
        private global: Global
    ) {
       this.ipaddress = (this._globalService.getCookie('ipaddress'))?this._globalService.getCookie('ipaddress'):'';
    }
        // Initialization method
    ngOnInit() {
        this.tabIndex = +this._globalService.getCookie('active_tabs'); // get current tab index
        this.parentId = this._globalService.getParentTab(this.tabIndex); // get parent tab id of current tab
        this.sub = this._route.params.subscribe(params => { //pick group id from the url and set to formModel
            this.formModel.groupId = +params['id']; // (+) converts string 'id' to a number
        });

        let websiteId = this._globalService.getWebsiteId();
        this.global.warehouseLoad(websiteId, this._globalService.getUserId()).subscribe(
            data => {
                this.warehouse_list = data.warehouse;
            },
            err => console.log(err),
            function() {
                //completed callback
            }
        );

        // Call group service at time of page load
        this._groupService.groupLoad(this.formModel.groupId).subscribe(data => {
            this.response = data;
            if (this.formModel.groupId > 0) { // While editing group
                this.formModel.groupId = this.response.api_status.grp.id;
                this.formModel.groupName = this.response.api_status.grp.name;
                this.menu_list = this.response.api_status.menu;
                let warehouseID = this.response.api_status.grp.warehouse_id;
                // this.formModel.warehouse_id = this.response.api_status.grp.warehouse_id;
                if(this.warehouse_list.some((item) => item.id == warehouseID)){
                    this.formModel.warehouse_id = warehouseID;
                }else{
                    this.formModel.warehouse_id = null;
                }
                this.menu_list.forEach(function(item: any) {
                    if (item.status == 1) {
                        item.Selected = true;
                    } else {
                        item.Selected = false;
                    }
                    item.child.forEach(function(child: any) {
                        if (child.status == 1) {
                            child.Selected = true;
                        } else {
                            child.Selected = false;
                        }
                    });
                });
            } else { //while adding a group
                this.menu_list = this.response.data;
                this.formModel.groupId = 0;
            }
        }, err => {
            this._globalService.showToast('Something went wrong. Please try again.');
        }, function() {
            //completed callback
        });
    }
        // destroy subscription variable
    ngOnDestroy() {
        this.sub.unsubscribe();
    }
        // onchange check all checkbox or Parent menu checkbox 

    getWebsitelist(){
        let post_data={
            "model":"EngageboostCompanyWebsites",
            "screen_name":"list",
            // "userid":this.userId,
            "search":"",
            "order_by":"",
            "order_type":"",
            "status":"",
            "website_id":this._globalService.getWebsiteId()}
            this.global.getWebServiceData('','POST',post_data,'').subscribe(data=>{
            
            })
    }
    
    checkMenuAll(parent: number, ev: any) {
        var flag: number = 0;
        let that = this;
        if (parent > 0) {
            this.menu_list.forEach(function(item: any, idx: number, array: any) {
                if (item.id == parent) {
                    item.child.forEach(function(child: any) {
                        child.Selected = item.Selected;
                    });
                }
                if (item.Selected) {
                    flag++;
                }
                if (idx === array.length - 1) { // check if it is last index
                    if (flag == array.length) {
                        that.checkAll = true;
                    } else {
                        that.checkAll = false;
                    }
                }
            });
        } else {
            this.menu_list.forEach(function(item: any) {
                item.Selected = ev.checked;
                item.child.forEach(function(child: any) {
                    child.Selected = item.Selected;
                });
            });
        }
    };
    // onchange child menu checkbox
    checkMenu(parent: number, ev: any) {
            let that = this;
            var flag: number = 0;
            this.menu_list.forEach(function(item: any, idx: number, array: any) {
                var sub_flag: number = 0;
                if (item.id == parent) {
                    item.child.forEach(function(child: any) {
                        if (child.Selected) {
                            sub_flag++;
                        }
                    });
                    if (sub_flag == item.child.length) {
                        item.Selected = true;
                    } else {
                        item.Selected = false;
                        that.checkAll = false;
                    }
                }
                if (item.Selected) {
                    flag++;
                }
                if (idx === array.length - 1) {
                    if (flag == array.length) {
                        that.checkAll = true;
                    } else {
                        that.checkAll = false;
                    }
                }
            });
        }
        // Form submit method
    addEditGroup(form: any) {
        this.errorMsg = '';
        var selectedMenu: any = [];
        this.menu_list.forEach(function(item: any) {
            if (item.Selected) {
                selectedMenu.push(item.id);
            }
            item.child.forEach(function(child: any) {
                if (child.Selected) {
                    selectedMenu.push(child.id);
                }
            });
        });
        if (selectedMenu.length > 0) {
            var data: any = {};
            data.company_id = 1;
            data.name = this.formModel.groupName;
            data.user_id = this._globalService.getUserId();
            data.masters = selectedMenu.join();            
            data.website_id = this._globalService.getWebsiteId();
            data.warehouse_id = this.formModel.warehouse_id;
            if (this.ipaddress) {
                data.ip_address = this.ipaddress;
            } else {
                data.ip_address = '';
            }
            if (this.formModel.groupId < 1) {
                data.createdby = this._globalService.getUserId();
            }
            data.language_id = 1;
            data.updatedby = this._globalService.getUserId();
            this._groupService.groupAddEdit(data, this.formModel.groupId).subscribe(data => {
                this.response = data;
                if (this.response.status == 1) {
                    this._router.navigate(['/groups']);
                    this._globalService.deleteTab(this.tabIndex, this.parentId);
                } else {
                    this.errorMsg = this.response.message;
                }
            }, err => {
                this._globalService.showToast('Something went wrong. Please try again.');
            }, function() {
                //completed callback
            });
        } else {
            this.errorMsg = 'Please select module permission';
        }
    }
}