import { Component, OnInit, OnDestroy  } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { RoleService } from './employee.role.service'; 
import { GlobalService } from '../../global/service/app.global.service';
import { Global } from '../../global/service/global';
import { AddEditTransition } from '../.././addedit.animation';

@Component({
    templateUrl: './templates/add_rolemasters.html',
    providers: [RoleService, Global],
    animations: [AddEditTransition],
    host: {
        '[@AddEditTransition]': ''
    },
})
export class RoleAddEditComponent implements OnInit, OnDestroy {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public masterlist: any = {};
    public grouplist: any;
    public formModel: any = {};
    private sub: any;
    public tabIndex: number;
    public parentId: number = 0;
    public ipaddress: any;
    public checkAll: boolean;
    public warehouse_list: any = [];
    constructor(private _roleService: RoleService, 
        public _globalService: GlobalService, private _router: Router,
        private _route: ActivatedRoute,
        private global: Global
        ) {
        this.ipaddress = _globalService.getCookie('ipaddress');
    }
    ngOnInit() {
        this.tabIndex = +this._globalService.getCookie('active_tabs');
        this.parentId = this._globalService.getParentTab(this.tabIndex);
        this.sub = this._route.params.subscribe(params => {
            this.formModel.roleId = +params['id']; // (+) converts string 'id' to a number
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

        this._roleService.roleLoad(this.formModel.roleId).subscribe(data => {
            this.response = data;
            if (this.formModel.roleId > 0) {
                this.formModel.roleId = this.response.api_status[0].addrule.id;
                this.formModel.roleName = this.response.api_status[0].addrule.name;
                this.grouplist = this.response.api_status[0].grp;
                this.masterlist = this.response.api_status[0].ruleset;
                this.formModel.status = this.response.api_status[0].addrule.isblocked;
                this.formModel.group = this.response.api_status[0].addrule.group_id;
                this.formModel.user_role_type = this.response.api_status[0].addrule.user_role_type;
                let warehouseID = this.response.api_status[0].addrule.warehouse_id;
                // this.formModel.warehouse_id = this.response.api_status[0].addrule.warehouse_id;
                if(this.warehouse_list.some((item) => item.id == warehouseID)){
                    this.formModel.warehouse_id = warehouseID;
                }else{
                    this.formModel.warehouse_id = null;
                }
                this.masterlist.forEach(function(item: any) {
                    if (item.add == 'Y') {
                        item.add = true;
                    } else {
                        item.add = false;
                    }
                    if (item.edit == 'Y') {
                        item.edit = true;
                    } else {
                        item.edit = false;
                    }
                    if (item.view == 'Y') {
                        item.view = true;
                    } else {
                        item.view = false;
                    }
                    if (item.delete == 'Y') {
                        item.delete = true;
                    } else {
                        item.delete = false;
                    }
                    if (item.block == 'Y') {
                        item.block = true;
                    } else {
                        item.block = false;
                    }
                    if (item.import_field == '1') {
                        item.import_field = true;
                    } else {
                        item.import_field = false;
                    }
                    if (item.export == '1') {
                        item.export = true;
                    } else {
                        item.export = false;
                    }
                    if (item.add && item.edit && item.view && item.delete && item.block && item.import_field && item.export) {
                        item.checkAll = true;
                    } else {
                        item.checkAll = false;
                    }
                });
            } else {
                this.grouplist = this.response;
                this.formModel.roleId = 0;
                this.formModel.status = 'n';
            }
        }, err => {
            this._globalService.showToast('Something went wrong. Please try again.');
        }, function() {
            //completed callback
        });
    }
    ngOnDestroy() {
        this.sub.unsubscribe();
    }
    getGroupPermissions(id: number) {
        if(id != null){
            this._roleService.getGroupPermissions(id).subscribe(data => {
                this.response = data;
                this.masterlist = this.response.data;
            }, err => {
                this._globalService.showToast('Something went wrong. Please try again.');
            }, function() {
                //completed callback
            });
        }
    }
    checkPermissionAll(master: number, ev: any) {
        var flag: number = 0;
        let that = this;
        if (master > 0) {
            this.masterlist.forEach(function(item: any, idx: number, array: any) {
                if (item.id == master) {
                    item.add = ev.checked;
                    item.edit = ev.checked;
                    item.view = ev.checked;
                    item.delete = ev.checked;
                    item.block = ev.checked;
                    item.import_field = ev.checked;
                    item.export = ev.checked;
                }
                if (item.checkAll) {
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
        } else {
            this.masterlist.forEach(function(item: any) {
                item.checkAll = ev.checked;
                item.add = ev.checked;
                item.edit = ev.checked;
                item.view = ev.checked;
                item.delete = ev.checked;
                item.block = ev.checked;
                item.import_field = ev.checked;
                item.export = ev.checked;
            });
        }
    }
    checkPermission(master: number, ev: any) {
        let that = this;
        var flag: number = 0;
        this.masterlist.forEach(function(item: any, idx: number, array: any) {
            if (item.id == master) {
                if (item.add && item.edit && item.view && item.delete && item.block && item.import_field && item.export) {
                    item.checkAll = true;
                } else {
                    item.checkAll = false;
                    that.checkAll = false;
                }
            }
            if (item.checkAll) {
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
    addEditRole(form: any) {
        this.errorMsg = '';
        var isvalid: number = 0;
        this.masterlist.forEach(function(item: any) {
            if (!item.add && !item.edit && !item.view && !item.delete && !item.block && !item.import_field && !item.export) {
                isvalid++;
            }
        });
        if (isvalid == this.masterlist.length) {
            this.errorMsg = 'Please select master permission';
        } else {
            this.errorMsg = '';
            var data: any = {};
            data.addrule = {};
            data.addrule.group_id = this.formModel.group;
            data.addrule.website_id = this._globalService.getWebsiteId();
            data.addrule.company_id = this._globalService.getCompanyId(); // company id coming from cookies
            data.addrule.user_role_type = this.formModel.user_role_type;
            data.addrule.name = this.formModel.roleName;
            data.addrule.isblocked = this.formModel.status;
            data.addrule.details = 1;
            data.website_id = this._globalService.getWebsiteId();
            if (this.ipaddress) {
                data.addrule.ip_address = this.ipaddress;
            } else {
                data.addrule.ip_address = '';
            }
            data.addrule.language_id = 1;
            if (this.formModel.groupId < 1) {
                data.createdby = this._globalService.getUserId();
            }
            data.warehouse_id = this.formModel.warehouse_id;
            
            data.updatedby = this._globalService.getUserId();
            data.ruleset = [];
            this.masterlist.forEach(function(item: any) {
                var rules: any = {};
                rules.master_id = item.id;
                rules.isdeleted = 0;
                rules.isblocked = 0;
                if (item.add) rules.add = 'Y';
                else rules.add = 'N';
                if (item.edit) rules.edit = 'Y';
                else rules.edit = 'N';
                if (item.delete) rules.delete = 'Y';
                else rules.delete = 'N';
                if (item.view) rules.view = 'Y';
                else rules.view = 'N';
                if (item.block) rules.block = 'Y';
                else rules.block = 'N';
                if (item.import_field) rules.import_field = '1';
                else rules.import_field = '0';
                if (item.export) rules.export = '1';
                else rules.export = '0';
                data.ruleset.push(rules);
            });                       
            this._roleService.roleAddEdit(data, this.formModel.roleId).subscribe(data => {
                this.response = data;
                if (this.response.status == 1) {
                    this._router.navigate(['/roles']);
                    this._globalService.deleteTab(this.tabIndex, this.parentId);
                } else {
                    this.errorMsg = this.response.message;
                }
            }, err => {
                this._globalService.showToast('Something went wrong. Please try again.');
            }, function() {
                //completed callback
            });
        }
    }
}