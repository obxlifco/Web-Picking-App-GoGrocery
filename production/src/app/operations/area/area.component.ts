import {Component, ElementRef, OnInit, Input, Inject, AfterViewInit, Optional } from '@angular/core';
import { GlobalService } from '../../global/service/app.global.service';
import { CookieService } from 'ngx-cookie';
import { Global } from '../../global/service/global';
import { Router, ActivatedRoute } from '@angular/router';
import { MatTooltipModule } from '@angular/material/tooltip';
import { DomSanitizer } from '@angular/platform-browser';
import { PaginationInstance } from 'ngx-pagination';
import { DialogsService } from '../../global/dialog/confirm-dialog.service';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { DOCUMENT } from '@angular/platform-browser';
import { GlobalVariable } from '../../global/service/global';
import { AddEditTransition, AddEditStepFlipTransition } from '../.././addedit.animation';
import { AreaService } from '../../operations/area/operation.area.service';
import { ColumnLayoutComponent } from '../../global/grid/app.grid-global.component';

@Component({
    selector: 'app-area',
    templateUrl: 'templates/area.component.html',
    styleUrls: ['area.component.css'],
    providers: [AreaService],
})

export class AreaComponent implements OnInit {
    public response: any;
    public errorMsg: string;
    public successMsg: string;
    public bulk_ids: any = [];
    public pagination: any = {};
    public pageIndex: number = 0;
    public pageList: number = 0;
    public sortBy: any = '';
    public sortOrder: any = '';
    public sortClass: any = '';
    public sortRev: boolean = false;
    public selectedAll: any = false;
    public stat: any = {};
    public result_list: any = [];
    public total_list: any = [];
    public cols: any = [];
    public layout: any = [];
    public add_btn: string;
    public post_data = {};
    page: number = 1;
    public filter: string = '';
    public maxSize: number = 10;
    public directionLinks: boolean = true;
    public autoHide: boolean = false;
    public config: any = {};
    public permission: any = [];
    public show_btn: any = {
        'add': true,
        'edit': true,
        'delete': true,
        'block': true
    };
    public userId: any;
    public individualRow: any = {};
    public search_text: any;
    public childData: any = {};
    public tabIndex: number;
    public parentId: number = 0;
    public locationType: any = 'Z';
    public colSpanCount:number=4;
    showSkeletonLoaded: boolean = false;
	public temp_result=[];
    public temp_col=[];
    public selectedTabIndex: number = 0;

    constructor(private globalService: GlobalService, private global: Global, private _router: Router, private sanitizer: DomSanitizer, private dialogsService: DialogsService, private elRef: ElementRef, private _cookieService: CookieService,private _AS:AreaService, public dialog: MatDialog, @Inject(DOCUMENT) private document: any) {
        this.tabIndex = +globalService.getCookie('active_tabs');
        this.parentId = globalService.getParentId(this.tabIndex);
    }

    ngOnInit() {
    	this.global.globalDataSet.subscribe(dataSet => {
            if(dataSet != 0) {
                this.locationType = dataSet;
            }
        }, err => {
          console.log(err);
        });

		this.global.setData(this.locationType);

        let userData = this._cookieService.getObject('userData');
        this.userId = userData['uid'];
        this.childData = {
            table: 'EngageboostZoneMasters',
            heading: 'Zone',
            ispopup: 'N',
            tablink: 'area_management',
            tabparrentid: this.parentId,
            screen: 'list_zone',
            is_import: 'Y',
            is_export: 'Y',
            url_link:'add_zone',
        }
        //this.generateGrid(0, '', '', '', '', this.locationType);
        this.loadMasterList(this.locationType);
        this.globalService.loadSkeletonChange$.subscribe(
			(value) => {
				this.showSkeletonLoaded = value;
			}
		);
        for (let i = 0; i < 15; i++) {
			this.temp_result.push(i);
		}
		for (let i = 0; i < 5; i++) {
			this.temp_col.push(i);
		}
    }

    loadGridData(event: any) {
        let selectedTab = event.index;
        this.selectedTabIndex = selectedTab;
        if (selectedTab == 0) { // All
            this.loadMasterList('Z')
        } else if (selectedTab == 1) { // Active
            this.loadMasterList('A')
        } else { // Inactive
            this.loadMasterList('S')
        }
    }

    dialogRefColumnLayout: MatDialogRef<ColumnLayoutComponent> | null;
    loadColumnLayout() {
        let data: any = {}
        data["column"] = this.cols;
        data["layout"] = this.layout;
        this.dialogRefColumnLayout = this.dialog.open(ColumnLayoutComponent, { data: data });
        this.dialogRefColumnLayout.afterClosed().subscribe(result => {
            if (result != undefined) {
                this.cols = result;
                this.updateGrid(0);
            }
        });
    }


    updateGrid(isdefault:any){
		this.global.doGridFilter(this.childData.table,isdefault,this.cols,this.childData.screen).subscribe(
			data => {
				this.response = data;
				this.generateGrid(0,'','','','',this.locationType);
			},
			err => console.log(err),
			function(){
			}
		);
	}	

    loadMasterList(locationType) {
    	if (locationType == 'A') {
            this.childData.heading = 'Area';
            this.childData.screen = 'list_area';
        } else if (locationType == 'S') {
            this.childData.heading = 'Sub Area';
            this.childData.screen = 'list_subarea';
        } else {
            this.childData.heading = 'Zone';
            this.childData.screen = 'list_zone';
        }
        this.global.setData(locationType);
        this.generateGrid(0, '', '', '', '', this.locationType);
    }

    clearMe() {
        this.generateGrid(0, '', '', '', '', this.locationType);
    }
    setpagecount() {
        this.generateGrid(0, '', '', '', this.search_text, this.locationType);
    }

    clearSearchData() {
        if (this.search_text == '') {
            this.generateGrid(0, '', '', '', this.search_text, this.locationType);
        }
    }

    


    generateGrid(reload: any, page: any, sortBy: any, filter: any, search: any, locatoinType: any) {
        setTimeout(() => {
            // this.globalService.showLoaderSpinner(true);
            this.globalService.skeletonLoader(true);
        });
        if (search == '') {
            this.search_text = '';
        } else {
        	this.search_text = search;
        }
        let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
        elements[0].classList.remove('show');
        this.bulk_ids = [];
        this.individualRow = {};
        this.total_list = [];
        this.selectedAll = false;
        this.filter = filter;
        this.sortBy = sortBy;
        if (sortBy != '' && sortBy != undefined) {
            if (this.sortRev) {
                this.sortOrder = '-'
                this.sortRev = !this.sortRev;
                this.sortClass = 'icon-down';
            } else {
                this.sortOrder = '+'
                this.sortRev = !this.sortRev;
                this.sortClass = 'icon-up';
            }
        }
        //this.globalService.showLoaderSpinner(true);
        this.post_data = {
            "model": this.childData.table,
            "screen_name": this.childData.screen,
            "userid": this.userId,
            "search": search,
            "order_by": sortBy,
            "order_type": this.sortOrder,
            "status": filter,
            'location_type': locatoinType,
            "website_id":this.globalService.getWebsiteId(),
        }
        this.global.doGrid(this.post_data, page).subscribe(
            data => {
                this.response = data;
                if (this.response.count > 0) {
                    this.result_list = this.response.results[0].result;
                    this.result_list.forEach(function(item: any) {
                        if (item.isblocked == 'n') {
                            item.isblocked = 'Active';
                        } else {
                            item.isblocked = 'Inactive';
                        }

                    })
                    for (let i = 0; i < this.response.count; i++) {
                        this.total_list.push(i);
                    }

                } else {
                    this.result_list = [];
                }

                this.layout = this.response.results[0].layout;
                this.cols = this.response.results[0].applied_layout;
                
                this.colSpanCount = this.cols.length;
                this.pagination.total_page = this.response.per_page_count;
                this.pageList = this.response.per_page_count;
                this.stat.active = this.response.results[0].active;
                this.stat.inactive = this.response.results[0].inactive;
                this.stat.all = this.response.results[0].all;
                this.add_btn = this.response.results[0].add_btn;
                this.config.currentPageCount = this.result_list.length
                this.config.currentPage = page
                this.config.itemsPerPage = this.response.page_size;
                this.permission = this.response.results[0].role_permission;
                // this.globalService.showLoaderSpinner(false);
                this.globalService.skeletonLoader(false);

            },
            err => console.log(err),
            function() {}
        );
    }

    exportData(locationType) {
    	console.log(locationType)
    	setTimeout(() => {
            this.globalService.showLoaderSpinner(true);
        });
        this._AS.exportData(this.search_text,locationType).subscribe(
             res => {
             	 //console.log(res);
                 var url = window.location.protocol + '//' + window.location.hostname + ':8085' + res['file_link'];
                 //console.log("============"+url+"============");
                 //console.log(url);
                 var a = document.createElement("a");
                 a.href = url;
                 a.download = 'zone-area-subarea.xls';
                 document.body.appendChild(a);
                 a.click();
                 document.body.removeChild(a);
                 setTimeout(() => {
		            this.globalService.showLoaderSpinner(false);
		        });
             },
             err => {
             	setTimeout(() => {
		            this.globalService.showLoaderSpinner(false);
		        });
                console.log("ERROR");
             }
         );
    }
    ////////////////////////////Check/Uncheck//////////////

    toggleCheckAll(event: any) {
        let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
        let that = this;
        //console.log(that.childData.table);
        that.bulk_ids = [];
        this.selectedAll = event.checked;
        this.result_list.forEach(function(item: any) {
            item.selected = event.checked;
            if (item.selected) {
                that.bulk_ids.push(item.id);
                elements[0].classList.add('show');
            } else {
                elements[0].classList.remove('show');
            }
        });
    }
    toggleCheck(id: any, event: any) {
            let elements: NodeListOf < Element > = this.document.getElementsByClassName('action-box');
            let that = this;
            //that.bulk_ids=[];
            this.result_list.forEach(function(item: any) {
                if (item.id == id) {
                    item.selected = event.checked;
                    if (item.selected) {
                        that.bulk_ids.push(item.id);
                        elements[0].classList.add('show');
                    } else {
                        let index = that.bulk_ids.indexOf(item.id);
                        that.bulk_ids.splice(index, 1);
                        if (that.bulk_ids.length == 0) {
                            elements[0].classList.remove('show');
                        }
                    }
                }
                if (that.bulk_ids.length == 1) {
                    that.bulk_ids.forEach(function(item_id: any) {
                        if (item_id == item.id) {
                            that.individualRow = item;
                        }
                    });
                }
                that.selectedAll = false;

            });
        }
        /////////////////////////Filter Grid//////////////////////

    updateStatusAll(type: number, id: number) {
    	console.log(id);
        let msg = '';
        let perm = '';
        let msgp = '';
        if (id) {
            let that = this;
            that.bulk_ids = [];
            that.bulk_ids.push(id);
            console.log(that.bulk_ids)
        }
       	
        if (type == 2) {
            msg = 'Do you really want to delete selected records?';
            perm = this.permission.delete;
            msgp = 'You have no permission to delete!';
        } else if (type == 1) {
            msg = 'Do you really want to block selected records?';
            perm = this.permission.block;
            msgp = 'You have no permission to block!';
        } else {
            msg = 'Do you really want to unblock selected records?';
            perm = this.permission.block;
            msgp = 'You have no permission to unblock!';
        }
        if (perm == 'Y') {
            if (this.bulk_ids.length > 0) {
                this.dialogsService.confirm('Warning', msg).subscribe(res => {
                    if (res) {
                        this.global.doStatusUpdate(this.childData.table, this.bulk_ids, type).subscribe(
                            data => {
                                this.response = data;
                                this.globalService.showToast(this.response.Message);
                                this.generateGrid(0, '', '', '', '', this.locationType);
                            },
                            err => console.log(err),
                            function() {}
                        );
                    }
                });
            } else {
                this.dialogsService.alert('Error', 'Select Atleast One Record!').subscribe(res => {});
            }
        } else {
            this.dialogsService.alert('Permission Error', msgp).subscribe(res => {});
        }
	}	

	dialogRefPromotionImport: MatDialogRef<ImportFileAreaComponent> | null;
	openImportBox(id: any) {
		if (this.childData.table == 'EngageboostZoneMasters') {
			this.dialogRefPromotionImport = this.dialog.open(ImportFileAreaComponent, { data: 'import_file' });
			this.dialogRefPromotionImport.afterClosed().subscribe(result => {			
				this.generateGrid(0, '', '', '', '', this.locationType);
			});
		}
	}
}


@Component({
	templateUrl: 'templates/import-area.html',
	providers: [AreaService]
})
export class ImportFileAreaComponent implements OnInit {
	public errorMsg: string = '';
	public formModel: any = {};
	public sample_xls: any;
	public sample_csv: any;
	public file_data: any;
	public website_id_new: any;
	public company_id_new: any;
	public importOpt: any;
	public file_selection_tool: any;

	constructor(private _globalService: GlobalService,
		private _areaService: AreaService,
		public dialog: MatDialog,
		private dialogRef: MatDialogRef<ImportFileAreaComponent>,
		@Optional() @Inject(MAT_DIALOG_DATA) public data: any
	) {
		this.formModel = Object.assign({}, this.data);
	}

	ngOnInit() {
		this.sample_xls = window.location.protocol + '//' + window.location.hostname + ':8085' + '/media/importfile/sample/import_file_area.xls';
		this.sample_csv = window.location.protocol + '//' + window.location.hostname + ':8085' + '/media/importfile/sample/import_file_area.csv';
		this.importOpt = 'xls';
		this.file_selection_tool = 'No file choosen';
	}

	importAreaFileXLS(e: Event) {
		console.log(e);
		let files: any = {};
		let target: HTMLInputElement = e.target as HTMLInputElement;
		for (let i = 0; i < target.files.length; i++) {
			let file_arr: any = [];

			let reader = new FileReader();
			reader.readAsDataURL(target.files[i]);
			reader.onload = (event) => {
				file_arr['url'] = event.srcElement['result']
			}
			file_arr['_file'] = target.files[i];
			files[this.data] = file_arr;
		}
		console.log(files);
		var filename = files.import_file._file.name;
		this.file_selection_tool = filename;

		this.file_data = files.import_file._file;
		let extn = filename.split(".").pop();
		if (extn == 'xls' || extn == 'xlsx') {
			//this.dialogRef.close(files);
		} else {
			this._globalService.showToast('Please choose XLS/XLSX file');
		}
	}

	closeDialog() {
		this.dialogRef.close();
	}

	saveFileDataImport(form: any) {
		this.website_id_new = this._globalService.getWebsiteId();
		this.company_id_new = this._globalService.getCompanyId();
		var form_data = new FormData();
		if(this.file_data!= undefined) {
			form_data.append("import_file", this.file_data);
			form_data.append('website_id', this.website_id_new);
			form_data.append('company_id', this.company_id_new);
			console.log(form_data);
			this._areaService.saveFileData(form_data).subscribe(
				data => {
					this.dialogRef.close();
				},
				err => console.log(err),
				function () {
					//completed callback

				} 
			);  
		} else {
			this._globalService.showToast('Please choose XLS/XLSX file');
		}
	}
} 
