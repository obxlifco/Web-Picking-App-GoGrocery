import { mergeMap, map, filter } from "rxjs/operators";
import { Component, OnInit, Inject } from "@angular/core";
import { Router, ActivatedRoute, NavigationEnd } from "@angular/router";
import { GlobalService } from "../../global/service/app.global.service";
import { Global } from "../../global/service/global";
import { CookieService } from "ngx-cookie";
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from "@angular/material";
import { PromotionService } from "../../products/promotion/products.promotion.service";
@Component({
  selector: "app-creditearncondition.addedit",
  templateUrl: "templates/creditearncondition.addedit.component.html",
  providers: [Global, PromotionService]
})
export class CreditearnconditionAddeditComponent implements OnInit {
  public response: any;
  public errorMsg: string;
  public successMsg: string;

  public discount_fields: any;
  public discount_conditions: any = [];
  public formModel: any = {};

  public tabIndex: number;
  public parentId: number = 0;
  public add_edit: any;
  public discount_master_type: number;
  constructor(
    private _promotionService: PromotionService,
    public _globalService: GlobalService,
    private _router: Router,
    private _route: ActivatedRoute,
    private _cookieService: CookieService,
    public dialog: MatDialog,
    private global: Global
  ) {
    //this.ipaddress = _globalService.getCookie('ipaddress');
    this.discount_fields = [
      {
        field: { name: "Category", value: 0 },
        condition: [
          { name: "Not Equals To", value: "!=" },
          { name: "Equals To", value: "==" }
        ],
        is_pop: 1
      },

      {
        field: { name: "SKU", value: 13633 },
        condition: [
          { name: "Not Equals To", value: "!=" },
          { name: "Equals To", value: "==" }
        ],
        is_pop: 1
      },

      {
        field: { name: "Order Amount", value: -1 },
        condition: [
          { name: "Equals To", value: "==" },
          { name: "Eqauls or less than", value: "<=" },
          { name: "Eqauls or Greater than", value: ">=" }
        ],
        is_pop: 0
      },
      {
        field: { name: "Customer", value: -2 },
        condition: [
          { name: "Not Equals To", value: "!=" },
          { name: "Equals To", value: "==" }
        ],
        is_pop: 1
      },
      {
        field: { name: "Customer Group", value: -3 },
        condition: [
          { name: "Not Equals To", value: "!=" },
          { name: "Equals To", value: "==" }
        ],
        is_pop: 1
      }
    ];

    this._router.events
      .pipe(
        filter(event => event instanceof NavigationEnd),
        map(() => this._route),
        map(route => {
          while (route.firstChild) route = route.firstChild;
          return route;
        }),
        filter(route => route.outlet === "primary"),
        mergeMap(route => route.data)
      )
      .subscribe(event => {
        this.discount_master_type = event["discountType"];
      });
  }
  ngOnInit() {
    this.tabIndex = +this._globalService.getCookie("active_tabs");
    this.parentId = this._globalService.getParentTab(this.tabIndex);

    this.add_edit = this._cookieService.getObject("action");

    if (this.add_edit == "add") {
      this.formModel.formId = this._cookieService.getObject("credit_point_add");
    } else {
      this.formModel.formId = this._cookieService.getObject("credit_point_edit");
    }
    this.formModel.discount_filters = [];
		this.formModel.discount_filters.push({});
    if (this.formModel.formId > 0) {
      this.global.getWebServiceData("loyaltyconditions","GET","",this.formModel.formId)
			.subscribe(
				data => {
					this.response = data.api_status;
						this.formModel.discount_filters = [];
						let that = this;
						if(data.status==1){
							this.response.forEach(function(item: any, index: number) {
								that.formModel.discount_filters.push({
									id: item.id,
									field: item.fields,
									condition: item.condition,
									conditionValues: item.value,
									all_product_id: item.all_product_id,
									all_customer_id: item.all_customer_id,
									all_category_id: item.all_category_id
								});
								that.get_conditions(item.fields, index);
							});
						}else{
							this.formModel.discount_filters.push({});
						}
				},
				err => {
					this._globalService.showToast(
						"Something went wrong. Please try again."
					);
				}
			);
		}
  }

  // Get conditions depending on a field
  get_conditions(value: any, index: number) {
    let that = this;
    this.discount_fields.forEach(function(item: any) {
      if (item.field.value == value) {
        that.discount_conditions[index] = item.condition;
        if (item.is_pop) {
          that.formModel.discount_filters[index]["is_pop"] = true;
        } else {
          that.formModel.discount_filters[index]["is_pop"] = false;
        }
      }
    });
  }
  change_value(value:any,index:number){
		this.discount_fields.forEach(element => {
			if(element.field.value==value){
				//this.formModel.discount_filters[index]['conditionValues'] = temp_value;
			}else{
				 this.formModel.discount_filters[index]['conditionValues']=null;
			}
		});
		
	}
  // Add more row
  addRow() {
    this.formModel.discount_filters.push({});
  }

  // Remove a row by index
  removeRow(index: number) {
    this.formModel.discount_filters.splice(index, 1);
  }

  // Add/Edit coupon conditions

  addEditCouponCondition(form: any) {
    this.errorMsg = "";
    var data: any = {};
    data.value = [];
    data["loyalty_master_id"] = this.formModel.formId;
    let that = this;
    this.formModel.discount_filters.forEach(function(item: any) {
      if (Object.keys(item).length) {
        let row = {};
        row["fields"] = item.field;
        row["loyalty_master_id"] = that.formModel.formId;
        row["condition"] = item.condition;
        row["value"] = item.conditionValues;
        if (item.field == 13633) {
          row["all_product_id"] = item.all_product_id
            ? item.all_product_id
            : null;
          row["all_customer_id"] = null;
          row["all_category_id"] = null;
        } else if (item.field == 0) {
          row["all_product_id"] = null;
          row["all_customer_id"] = null;
          row["all_category_id"] = item.all_category_id
            ? item.all_category_id
            : null;
        } else if (item.field == -2 || item.field == -3) {
          row["all_product_id"] = null;
          row["all_customer_id"] = item.all_customer_id
            ? item.all_customer_id
            : null;
          row["all_category_id"] = null;
        }
        row["condition_type"] = "AND";
        data.value.push(row);
      }
    });

    if (data.value.length > 0) {
      this._promotionService.conditionPointAddEdit(data, this.formModel.formId)
        .subscribe(
          data => {
            this.response = data;
            if (this.response.status == 1) {
              this._globalService.deleteTab(this.tabIndex, this.parentId);
              if (this.add_edit == "add") {
                this._cookieService.remove("action");
                this._cookieService.remove("credit_point_add");
                this._globalService.showToast(data["message"]);
                this._router.navigate(["/credit_points_earn"]);
              } else {
                this._cookieService.remove("action");
                this._cookieService.remove("credit_point_edit");
                this._router.navigate(["/credit_points_earn"]);
              }
            } else {
              this.errorMsg = this.response.message;
            }
          },
          err => {
            this._globalService.showToast(
              "Something went wrong. Please try again."
            );
          },
          function() {
            //completed callback
          }
        );
    } else {
      this._cookieService.remove("action");
      this._cookieService.remove("credit_point_edit");
      if (this.discount_master_type) {
        this._router.navigate(["/discount_coupan"]);
      } else {
        this._router.navigate(["/discount_product"]);
      }
    }
  }

  // condition popup references
  dialogCategoryRef: MatDialogRef<PointCategoryListComponent> | null;
  dialogProductRef: MatDialogRef<PointProductListComponent> | null;
  dialogCustomerGroupRef: MatDialogRef<PointCustomerGroupListComponent> | null;
  dialogCustomerRef: MatDialogRef<PointCustomerListComponent> | null;
  openPop(type: number, index: number) {
    let data: any = {};
    data["index"] = index;
    if (type == 0) {
      // Category

      data["condition_id"] = this.formModel.discount_filters[index]["id"];
      this.dialogCategoryRef = this.dialog.open(PointCategoryListComponent, {
        data: data
      });
      this.dialogCategoryRef.afterClosed().subscribe(result => {
        if (result) {
          this.formModel.discount_filters[result["index"]]["all_category_id"] =
            result["category_ids"];
          this.formModel.discount_filters[result["index"]]["conditionValues"] =
            result["category_names"];
        }
      });
    } else if (type == 13633) {
      // Sku

      data["all_product_id"] = this.formModel.discount_filters[index][
        "all_product_id"
      ];
      this.dialogProductRef = this.dialog.open(PointProductListComponent, {
        data: data
      });
      this.dialogProductRef.afterClosed().subscribe(result => {
        if (result) {
          this.formModel.discount_filters[result["index"]]["all_product_id"] =
            result["product_ids"];
          this.formModel.discount_filters[result["index"]]["conditionValues"] =
            result["product_names"];
        }
      });
    } else if (type == -2) {
      // Customer

      data["all_customer_id"] = this.formModel.discount_filters[index][
        "all_customer_id"
      ];
      this.dialogCustomerRef = this.dialog.open(PointCustomerListComponent, {
        data: data
      });
      this.dialogCustomerRef.afterClosed().subscribe(result => {
        if (result) {
          this.formModel.discount_filters[result["index"]]["all_customer_id"] =
            result["customer_ids"];
          this.formModel.discount_filters[result["index"]]["conditionValues"] =
            result["customer_names"];
        }
      });
    } else if (type == -3) {
      // Customer type

      data["all_customer_id"] = this.formModel.discount_filters[index][
        "all_customer_id"
      ];
      this.dialogCustomerGroupRef = this.dialog.open(
        PointCustomerGroupListComponent,
        { data: data }
      );
      this.dialogCustomerGroupRef.afterClosed().subscribe(result => {
        if (result) {
          this.formModel.discount_filters[result["index"]]["all_customer_id"] =
            result["customer_grp_ids"];
          this.formModel.discount_filters[result["index"]]["conditionValues"] =
            result["customer_grp_names"];
        }
      });
    }
  }
}

@Component({
  templateUrl: "./templates/coupon_conditions_category.html",
  providers: [PromotionService]
})
export class PointCategoryListComponent implements OnInit {
  public formModel: any = {};
  public response: any;
  public parent_category_list: any = [];
  public child_category_list: any = [];
  public sub_child_category_list: any = [];
  public sub_sub_child_category_list: any = [];
  constructor(
    public _globalService: GlobalService,
    private _promotionService: PromotionService,
    public dialog: MatDialog,
    private dialogRef: MatDialogRef<PointCategoryListComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {
    this.formModel.select_category = 1;
  }

  ngOnInit() {
    this._promotionService.categoryLoad(this.data.condition_id)
      .subscribe(
        data => {
          if (this.data.condition_id) {
            this.response = data;
            this.formModel.parent_categories = Object.assign(
              [],
              this.response.parent_child
            );
            this.parent_category_list = this.response.category;
            let that = this;
            this.formModel.parent_categories.forEach(function(
              item: any,
              index: number
            ) {
              if (item.category_4) {
                that.get_child_categories(item.category_1, index, 1, 0);
                that.get_child_categories(item.category_2, index, 2, 0);
                that.get_child_categories(item.category_3, index, 3, 0);
              } else if (item.category_3) {
                that.get_child_categories(item.category_1, index, 1, 0);
                that.get_child_categories(item.category_2, index, 2, 0);
                that.get_child_categories(item.category_3, index, 3, 0);
              } else if (item.category_2) {
                that.get_child_categories(item.category_1, index, 1, 0);
                that.get_child_categories(item.category_2, index, 2, 0);
              } else {
                if (item.category_1) {
                  that.get_child_categories(item.category_1, index, 1, 0);
                }
              }
            });
          } else {
            this.response = data;
            this.formModel.parent_categories = [{}];
            this.parent_category_list = this.response.category;
          }
        },
        err => {
          this._globalService.showToast(
            "Something went wrong. Please try again."
          );
        },
        function() {
          //completed callback
        }
      );
  }

  closeDialog() {
    this.dialogRef.close();
  }

  // Add more row
  addRow() {
    this.formModel.parent_categories.push({});
  }

  // Remove a row by index
  removeRow(index: number) {
    this.formModel.parent_categories.splice(index, 1);
    this.child_category_list.splice(index, 1);
    this.sub_child_category_list.splice(index, 1);
    this.sub_sub_child_category_list.splice(index, 1);
  }

  saveCategory() {
    let returnData: any = [];
    returnData["index"] = this.data.index;

    let category_ids: any = [];
    let categroy_names: any = [];

    let that = this;
    if (this.formModel.select_category == 1) {
      this.formModel.parent_categories.forEach(function(
        item: any,
        index: number
      ) {
        if (item.category_4) {
          category_ids.push(item.category_4);
          if (that.sub_sub_child_category_list[index].length) {
            that.sub_sub_child_category_list[index].forEach(function(
              child: any,
              index: number
            ) {
              if (child.id == item.category_4) {
                categroy_names.push(child.name);
              }
            });
          }
        } else if (item.category_3) {
          category_ids.push(item.category_3);
          if (that.sub_child_category_list[index].length) {
            that.sub_child_category_list[index].forEach(function(
              child: any,
              index: number
            ) {
              if (child.id == item.category_3) {
                categroy_names.push(child.name);
              }
            });
          }
        } else if (item.category_2) {
          category_ids.push(item.category_2);
          if (that.child_category_list[index].length) {
            that.child_category_list[index].forEach(function(
              child: any,
              index: number
            ) {
              if (child.id == item.category_2) {
                categroy_names.push(child.name);
              }
            });
          }
        } else {
          category_ids.push(item.category_1);
          if (that.parent_category_list.length) {
            that.parent_category_list.forEach(function(
              child: any,
              index: number
            ) {
              if (child.id == item.category_1) {
                categroy_names.push(child.name);
              }
            });
          }
        }
      });

      returnData["category_ids"] = category_ids.join(",");
      returnData["category_names"] = categroy_names.join(",");

      this.dialogRef.close(returnData);
    } else {
      this._promotionService.allCategoryLoad().subscribe(data => {
        this.response = data;
        let that = this;
        this.response.category.forEach(function(item: any, index: number) {
          category_ids.push(item.id);
          categroy_names.push(item.name);
        });

        returnData["category_ids"] = category_ids.join(",");
        returnData["category_names"] = categroy_names.join(",");

        this.dialogRef.close(returnData);
      }, err => {
        this._globalService.showToast(
          "Something went wrong. Please try again."
        );
      }, function() {
        //completed callback
      });
    }
  }

  get_child_categories(
    parent_id: number,
    index: number,
    lvl: number,
    reset: number
  ) {
    this._promotionService.getChildCategory(parent_id, 0, lvl + 1)
      .subscribe(
        data => {
          this.response = data;
          if (this.response.status) {
            if (lvl == 1) {
              //level 1 category
              if (reset == 0) {
                this.child_category_list[index] = this.response.category;
              } else {
                this.child_category_list[index] = [];
                this.sub_child_category_list[index] = [];
                this.sub_sub_child_category_list[index] = [];
                this.child_category_list[index] = this.response.category;
                this.formModel.parent_categories[index].category_2 = 0;
                this.formModel.parent_categories[index].category_3 = 0;
                this.formModel.parent_categories[index].category_4 = 0;
              }
            } else if (lvl == 2) {
              //level 2 category

              if (reset == 0) {
                this.sub_child_category_list[index] = this.response.category;
              } else {
                this.sub_child_category_list[index] = [];
                this.sub_sub_child_category_list[index] = [];
                this.sub_child_category_list[index] = this.response.category;
                this.formModel.parent_categories[index].category_3 = 0;
                this.formModel.parent_categories[index].category_4 = 0;
              }
            } else {
              //level 3 category
              if (reset == 0) {
                this.sub_sub_child_category_list[
                  index
                ] = this.response.category;
              } else {
                this.sub_sub_child_category_list[index] = [];
                this.sub_sub_child_category_list[
                  index
                ] = this.response.category;
                this.formModel.parent_categories[index].category_4 = 0;
              }
            }
          } else {
          }
        },
        err => {
          this._globalService.showToast(
            "Something went wrong. Please try again."
          );
        },
        function() {
          //completed callback
        }
      );
  }
}

@Component({
  templateUrl: "./templates/coupon_conditions_product.html",
  providers: [PromotionService]
})
export class PointProductListComponent implements OnInit {
  public product_list: any = [];
  public response: any;
  public selectedAll: boolean;
  public bulk_ids: any = [];
  public search_text: string;
  public sortBy: any = "";
  public sortOrder: any = "";
  public sortClass: any = "";
  public sortRev: boolean = false;
  public customerGrp_list: any = [];
  public errorMsg: string;
  public successMsg: string;
  public bulk_ids_exist: any = [];
  public pagination:any = {};
  public pageIndex : number = 0;
  public pageList : number = 0;
  public website_id:number = 1;
  public stat:any = {};
  public result_list:any=[];
  public total_list:any=[];
  public cols:any=[]
  public post_data = {};
  public page: number = 1;
  public filter: string = '';
  public maxSize: number = 10;
  public directionLinks: boolean = true;
  public autoHide: boolean = false;
  public config: any = {};
  public customers: any = [];
  public formModel: any = {};
  public userId: number;

  constructor(
    public _globalService: GlobalService,
    private _promotionService: PromotionService,
    public dialog: MatDialog,
    private dialogRef: MatDialogRef<PointProductListComponent>,
    private _cookieService: CookieService,

    @Inject(MAT_DIALOG_DATA) public data: any
  ) {}

  ngOnInit() {
    if (this.data["all_product_id"]) {
      this.bulk_ids = this.data["all_product_id"].split(",").map(Number);
    }

    // this.reload("", "id");
    this.generateGrid(0, '', '', '', '');

  }

  closeDialog() {
    this.dialogRef.close();
  }
  ////////////////////////////Check/Uncheck//////////////
  generateGrid(reload: any, page: any, sortBy: any, filter: any, search: any) {
    this.sortBy = sortBy;

    if (sortBy != "" && sortBy != undefined) {
        if (this.sortRev) {
            this.sortOrder = "-";
            this.sortRev = !this.sortRev;
            this.sortClass = "icon-down";
        } else {
            this.sortOrder = "+";
            this.sortRev = !this.sortRev;
            this.sortClass = "icon-up";
        }
    }

    let userData = this._cookieService.getObject('userData');
    this.userId = userData['uid'];

    let data = {
        "model": 'EngageboostProducts',
        "screen_name": 'list',
        "userid": this.userId,
        "search": this.search_text,
        "order_by": sortBy,
        "order_type": this.sortOrder,
        "status": 'n',
        "visibility_id":"Category,Search",
        "website_id": this._globalService.getWebsiteId()
    }

    this._promotionService.productLoad(data,page).subscribe(
        data => {
          let that = this;
          this.response = data;
          this.total_list = [];
            
          if(this.response.count > 0) {
            this.result_list = this.response.results[0].result;
            this.result_list.forEach(function(item:any){
                if(that.bulk_ids.indexOf(item.id)>-1){
                    item.Selected = true;
                }
            });
            for (var i = 0; i < this.response.count; i++) {
                this.total_list.push(i);
            }
          } else {
            this.result_list = [];
          }
          this.pagination.total_page = this.response.per_page_count;
          this.pageList = this.response.per_page_count;
          this.config.currentPageCount = this.result_list.length
          this.config.currentPage = page
          this.config.itemsPerPage = this.response.page_size;
        },
        err => {
          this._globalService.showToast('Something went wrong. Please try again.');
        },
        function(){
          //completed callback
        }
    );
  }
  toggleCheckAll(event: any) {
    let that = this;
    that.bulk_ids = [];
    this.selectedAll = event.checked;
    this.result_list.forEach(function(item: any) {
      item.Selected = event.checked;
      if (item.Selected) {
        that.bulk_ids.push(item.id);
      }
    });
  }

  toggleCheck(id: any, event: any) {
    let that = this;
    this.result_list.forEach(function(item: any) {
      if (item.id == id) {
        item.Selected = event.checked;
        if (item.Selected) {
          that.bulk_ids.push(item.id);
        } else {
          var index = that.bulk_ids.indexOf(item.id);
          that.bulk_ids.splice(index, 1);
        }
      }
    });
  }

  saveSku() {
    let returnData: any = [];
    returnData["index"] = this.data.index;

    let product_ids: string = "";
    let product_names: string = "";
    let products: any = [];

    product_ids = this.bulk_ids.join(",");

    let that = this;
    this.bulk_ids.forEach(function(item: any) {
      that.result_list.forEach(function(inner_item: any) {
        if (item == inner_item.id) {
          products.push(inner_item.sku);
        }
      });
    });

    product_names = products.join(",");

    returnData["product_ids"] = product_ids;
    returnData["product_names"] = product_names;

    this.dialogRef.close(returnData);
  }
}

@Component({
  templateUrl: "./templates/coupon_conditions_customers.html",
  providers: [PromotionService]
})
export class PointCustomerListComponent implements OnInit {
  public customer_list: any = [];
  public response: any;
  public selectedAll: boolean;
  public bulk_ids: any = [];
  public search_text: string;
  public sortBy: any = "";
  public sortOrder: any = "";
  public sortClass: any = "";
  public sortRev: boolean = false;
  public errorMsg: string;
  public successMsg: string;
  public bulk_ids_exist: any = [];
  public pagination:any = {};
  public pageIndex : number = 0;
  public pageList : number = 0;
  public website_id:number = 1;
  public stat:any = {};
  public result_list:any=[];
  public total_list:any=[];
  public cols:any=[]
  public post_data = {};
  public page: number = 1;
  public filter: string = '';
  public maxSize: number = 10;
  public directionLinks: boolean = true;
  public autoHide: boolean = false;
  public config: any = {};
  public customers: any = [];
  public formModel: any = {};
  public userId: number;

  constructor(
    public _globalService: GlobalService,
    private _promotionService: PromotionService,
    public dialog: MatDialog,
    private dialogRef: MatDialogRef<PointCustomerListComponent>,
    private _cookieService: CookieService,

    @Inject(MAT_DIALOG_DATA) public data: any
  ) {}

  ngOnInit() {
    if (this.data["all_customer_id"]) {
      this.bulk_ids = this.data["all_customer_id"].split(",").map(Number);
    }

    this.generateGrid(0, '', '', '', '');
  }

  closeDialog() {
    this.dialogRef.close();
  }

  // reload(search_key: string, sortBy: string){
  generateGrid(reload: any, page: any, sortBy: any, filter: any, search: any) {
    this.sortBy = sortBy;

    if (sortBy != "" && sortBy != undefined) {
        if (this.sortRev) {
            this.sortOrder = "-";
            this.sortRev = !this.sortRev;
            this.sortClass = "icon-down";
        } else {
            this.sortOrder = "+";
            this.sortRev = !this.sortRev;
            this.sortClass = "icon-up";
        }
    }

    let userData = this._cookieService.getObject('userData');
    this.userId = userData['uid'];

    let data = {
        "model": 'EngageboostCustomers',
        "screen_name": 'list',
        "userid": this.userId,
        "search": this.search_text,
        "order_by": sortBy,
        "order_type": this.sortOrder,
        "status": 'n',
        "website_id": this._globalService.getWebsiteId()
    }

    this._promotionService.customerLoad(data,page).subscribe(
        data => {
          let that = this;
          this.response = data;
          this.total_list = [];
            
          if(this.response.count > 0) {
            this.result_list = this.response.results[0].result;
            this.result_list.forEach(function(item:any){
                if(that.bulk_ids.indexOf(item.id)>-1){
                    item.Selected = true;
                }
            });
            for (var i = 0; i < this.response.count; i++) {
                this.total_list.push(i);
            }
          } else {
            this.result_list = [];
          }
          this.pagination.total_page = this.response.per_page_count;
          this.pageList = this.response.per_page_count;
          this.config.currentPageCount = this.result_list.length
          this.config.currentPage = page
          this.config.itemsPerPage = this.response.page_size;
        },
        err => {
          this._globalService.showToast('Something went wrong. Please try again.');
        },
        function(){
          //completed callback
        }
    );
  }

  ////////////////////////////Check/Uncheck//////////////

  toggleCheckAll(event: any) {
    let that = this;
    that.bulk_ids = [];
    this.selectedAll = event.checked;
    this.result_list.forEach(function(item: any) {
      item.Selected = event.checked;
      if (item.Selected) {
        that.bulk_ids.push(item.id);
      }
    });
  }

  toggleCheck(id: any, event: any) {
    let that = this;
    this.result_list.forEach(function(item: any) {
      if (item.id == id) {
        item.Selected = event.checked;
        if (item.Selected) {
          that.bulk_ids.push(item.id);
        } else {
          var index = that.bulk_ids.indexOf(item.id);
          that.bulk_ids.splice(index, 1);
        }
      }
    });
  }

  saveCustomers() {
    let returnData: any = [];
    returnData["index"] = this.data.index;

    let customer_ids: string = "";
    let customer_names: string = "";
    let customers: any = [];

    customer_ids = this.bulk_ids.join(",");

    let that = this;
    this.bulk_ids.forEach(function(item: any) {
      that.result_list.forEach(function(inner_item: any) {
        if (item == inner_item.id) {
          customers.push(inner_item.first_name + " " + inner_item.last_name);
        }
      });
    });

    customer_names = customers.join(",");

    returnData["customer_ids"] = customer_ids;
    returnData["customer_names"] = customer_names;

    this.dialogRef.close(returnData);
  }
}

@Component({
  templateUrl: "./templates/coupon_conditions_customerGroups.html",
  providers: [PromotionService]
})
export class PointCustomerGroupListComponent implements OnInit {
  public customerGrp_list: any = [];
  public response: any;
  public selectedAll: boolean;
  public bulk_ids: any = [];
  public search_text: string;
  public sortBy: any = "";
  public sortOrder: any = "";
  public sortClass: any = "";
  public sortRev: boolean = false;
  public errorMsg: string;
  public successMsg: string;
  public bulk_ids_exist: any = [];
  public pagination:any = {};
  public pageIndex : number = 0;
  public pageList : number = 0;
  public website_id:number = 1;
  public stat:any = {};
  public result_list:any=[];
  public total_list:any=[];
  public cols:any=[]
  public post_data = {};
  public page: number = 1;
  public filter: string = '';
  public maxSize: number = 10;
  public directionLinks: boolean = true;
  public autoHide: boolean = false;
  public config: any = {};
  public customers: any = [];
  public formModel: any = {};
  public userId: number;

  constructor(
    public _globalService: GlobalService,
    private _promotionService: PromotionService,
    public dialog: MatDialog,
    private dialogRef: MatDialogRef<PointCustomerGroupListComponent>,
    private _cookieService: CookieService,
    @Inject(MAT_DIALOG_DATA) public data: any
  ) {}

  ngOnInit() {
    if (this.data["all_customer_id"]) {
      this.bulk_ids = this.data["all_customer_id"].split(",").map(Number);
    }
    this.generateGrid(0, '', '', '', '');
    
  }

  closeDialog() {
    this.dialogRef.close();
  }

  generateGrid(reload: any, page: any, sortBy: any, filter: any, search: any) {
    this.sortBy = sortBy;

    if (sortBy != "" && sortBy != undefined) {
        if (this.sortRev) {
            this.sortOrder = "-";
            this.sortRev = !this.sortRev;
            this.sortClass = "icon-down";
        } else {
            this.sortOrder = "+";
            this.sortRev = !this.sortRev;
            this.sortClass = "icon-up";
        }
    }

    let userData = this._cookieService.getObject('userData');
    this.userId = userData['uid'];

    let data = {
        "model": 'EngageboostCustomerGroup',
        "screen_name": 'list',
        "userid": this.userId,
        "search": this.search_text,
        "order_by": sortBy,
        "order_type": this.sortOrder,
        "status": 'n',
        "website_id": this._globalService.getWebsiteId()
    }

    this._promotionService.customerLoad(data,page).subscribe(
        data => {
          let that = this;
          this.response = data;
          this.total_list = [];
            
          if(this.response.count > 0) {
            this.result_list = this.response.results[0].result;
            this.result_list.forEach(function(item:any){
                if(that.bulk_ids.indexOf(item.id)>-1){
                    item.Selected = true;
                }
            });
            for (var i = 0; i < this.response.count; i++) {
                this.total_list.push(i);
            }
          } else {
            this.result_list = [];
          }
          this.pagination.total_page = this.response.per_page_count;
          this.pageList = this.response.per_page_count;
          this.config.currentPageCount = this.result_list.length
          this.config.currentPage = page
          this.config.itemsPerPage = this.response.page_size;
        },
        err => {
          this._globalService.showToast('Something went wrong. Please try again.');
        },
        function(){
          //completed callback
        }
    );
  }

  // Check/Uncheck
  toggleCheckAll(event: any) {
    let that = this;
    that.bulk_ids = [];
    this.selectedAll = event.checked;
    this.result_list.forEach(function(item: any) {
      item.Selected = event.checked;
      if (item.Selected) {
        that.bulk_ids.push(item.id);
      }
    });
  }

  toggleCheck(id: any, event: any) {
    let that = this;
    this.result_list.forEach(function(item: any) {
      if (item.id == id) {
        item.Selected = event.checked;
        if (item.Selected) {
          that.bulk_ids.push(item.id);
        } else {
          var index = that.bulk_ids.indexOf(item.id);
          that.bulk_ids.splice(index, 1);
        }
      }
    });
  }

  saveCustomerGroup() {
    let returnData: any = [];
    returnData["index"] = this.data.index;

    let customer_grp_ids: string = "";
    let customer_grp_names: string = "";
    let customer_grps: any = [];

    customer_grp_ids = this.bulk_ids.join(",");

    let that = this;
    this.bulk_ids.forEach(function(item: any) {
      that.result_list.forEach(function(inner_item: any) {
        if (item == inner_item.id) {
          customer_grps.push(inner_item.name);
        }
      });
    });

    customer_grp_names = customer_grps.join(",");

    returnData["customer_grp_ids"] = customer_grp_ids;
    returnData["customer_grp_names"] = customer_grp_names;

    this.dialogRef.close(returnData);
  }
}
