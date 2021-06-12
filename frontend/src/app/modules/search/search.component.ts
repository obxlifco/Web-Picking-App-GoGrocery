import { Component, OnInit, SimpleChanges, ElementRef, Inject, ViewChild, Output, EventEmitter, PLATFORM_ID } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CookieService } from 'ngx-cookie';
import { Global } from '../../global/service/global';
import { GlobalService } from '../../global/service/app.global.service';
import { SearchService } from '../../global/service/search.service';
import { CartService } from '../../global/service/cart.service';
import { WarehouseService } from '../../global/service/warehouse.service';
import { ProductService } from '../../global/service/product.service';
import { AuthenticationService } from '../../global/service/authentication.service';
import { LoginComponent } from '../../login/login.component';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';
import { Options } from 'ng5-slider';
import {MenuService} from '../../global/service/menu.service';
import { WINDOW,LOCAL_STORAGE} from '@ng-toolkit/universal';


import {
  Location,
  LocationStrategy,
  HashLocationStrategy,
  APP_BASE_HREF,
  isPlatformBrowser
} from '@angular/common';

@Component({
  selector: 'app-search',
  providers: [Location, { provide: LocationStrategy, useClass: HashLocationStrategy }],
  templateUrl: './template/search.component.html',
  styleUrls: ['./search.component.css']
})

export class SearchComponent implements OnInit {
  @ViewChild('filterBox') filterBox: ElementRef;
  @ViewChild('sortBox') sortBox: ElementRef;
  public subCat:any=[];
  public subBrand:any=[];
  public subSize:any=[];
  public category_id: any;
  public category_slug = '';
  public brand_slug = '';
  public product_list = [];
  public variations_value = [];
  // selected = "";
  public all_product = [];
  public config: any = {};
  public total_list = [];
  public priceRangeMinimumValue;
  public priceRangeMaximumValue;
  public selectedPriceRange = 0;
  public sliderOption = {};
  public objectKeys = Object.keys;
  public defaultExpanded:boolean = true;
  public search_ids = [];
  public searchIdString = '';
  public searchKeyword = '';
  public totalNoOfItem = 0;
  public throttle = 50;
  public scrollDistance = 1.5;
  public scrollUpDistance = 2;
  p: any;
  from:any = 0;
  sorting_data: any = [];
  filter_data_non_variation = [];
  filter_data_variation = [];
  filter_price = [];
  sorting_selected = "New Arrivals";
  warehouse_id: any;
  // breadcrumbs = [];
  page_size: any;

  totalCount: any;
  sub: any;
  filter_selected = [];
  breadcrumbs = [];
  // brand_selected = "";
  // selected_variation_name: any;FelasticData
  // selected_variation_value: any;
  public maxSize: number = 10;
  public pagination: any = {};
  public savelist_data = [];
  public formModel:any={};
  public isPriceFilter:boolean=false;
  public mobile_bredcumb:any='';
  constructor(
    @Inject(WINDOW) private window: Window,
    @Inject(LOCAL_STORAGE) private localStorage: any,
    private _route: ActivatedRoute,
    private global: Global,
    private router: Router,
    private _cookieService: CookieService,
    private location: Location,
    private _globalService: GlobalService,
    private _warehouseService: WarehouseService,
    private _productService: ProductService,
    public cartService: CartService,
    public dialog: MatDialog,
    public authenticationService: AuthenticationService,
    private _menuservice:MenuService,
    private _searchService:SearchService,
    @Inject(PLATFORM_ID) private platformId: Object

  ) {

    
  }

  ngOnInit() {
    // Subsribe to warehouse for getting any change any warehouse
    if (isPlatformBrowser(this.platformId)) {
      this._warehouseService.warehouseData$.subscribe(response => {
        this.warehouse_id = response['selected_warehouse_id'];
        let name = '';
        this.page_size = 18; //this._cookieService.getObject('globalData')['pagesize'] ? this._cookieService.getObject('globalData')['pagesize'] : 18;
        let encrypteparm = [];
        this._route.queryParams.subscribe(response => {
            this.searchIdString = response && response['v'] ? decodeURIComponent(response['v']) : '';
            this.searchKeyword  = response && response['q'] ? decodeURI(response['q']) : '';
            if(this.searchIdString) {
              this.resetListing();
              let decodedSearchIdString = atob(this.searchIdString);
              this.search_ids = decodedSearchIdString.split(',');
              this.getListingdata(this.searchIdString);
              let filter_set = this.elasticData();
              this.showElasticDataInUI(filter_set);
            }
        });
      });

    }
  }
  getListingdata(name) {
    //alert(name);
    let filterType = this.brand_slug ? 'brand' : 'category';
    this._globalService.showLoaderSpinner(true);
    let encrypteparm = [];
    this.variations_value = [];
    // selected = "";
    this.all_product = [];
    this.config = {};
    this.pagination = {};
    this.total_list = [];
    this.sorting_data = [];
    //this.sorting_selected = "";
    let type = 'category';
    this.filter_selected = [];
    this.breadcrumbs = [];
    /*this._productService.getIdFromSlug(name).subscribe(response => {
      if (response && response['status'] == 1) {
        this.queryParamRemove();
      } else {
        if (this._route.snapshot.queryParams['search']) {
          this._route.queryParams.subscribe(params => {
            if (params['search']) {
              let encryptedobject = JSON.parse(atob(params['search']));
              encrypteparm.push(encryptedobject);
            }
          })
        }
      }
    })*/
    
    /*this.global.getCateoryBannerWithSorting(name,filterType).subscribe(data => {
      if (data.status == 1) {
        this.sorting_data = data.sort_by;
        this.breadcrumbs = data.breadcrumb;
        this.breadcrumbs.forEach((element,index) => {
          if(this.breadcrumbs.length -1 ==index){
            this.mobile_bredcumb=element.name;
          }
        });
        this.category_id = data.category_id;
        this.sorting_data.forEach(sort => {
          if (sort.name == "New Arrivals")
            this.sorting_selected = sort.name.toString();
          //console.log(this.sorting_selected);
        });
      }
    })*/

    // if(!this.brand_slug){
    this._searchService.getFilterDataByProductId(name).subscribe(result => {
      this.filter_data_non_variation = [];
      this.filter_data_variation = [];
      this.filter_price = [];

      result.forEach(item => {
        if (item.status == 0) {
          this._globalService.showLoaderSpinner(false);
          //this._globalService.showToast('Product is not available in this category');
        } else {
          this._globalService.showLoaderSpinner(false);
         
          if (item.child.length > 0 && item.field_name == "price") {
            this.sliderOption = {
              floor : 0,
              ceil : item['max_price'],
              step: 1,
              showTicks: true

            }
            this.filter_price.push(item);
            this.filter_price.map(item => {
              if (item.child.length > 0) {
                item.child.map(x => {
                  x['is_checked'] = false;

                })
              }
            })
          } else if(item.child.length > 0 && item.field_name == "sort_by") {
            this.sorting_data = item.child;


          } else {
            if (item.is_variant == "true" && item.child.length > 0) {
              this.filter_data_variation.push(item);
              this.filter_data_variation.map(item => {
                if (item.child.length > 0) {
                  item.child.map(x => {
                    x['is_checked'] = false;
                    x['item_type'] = item.field_name;
                  })
                }
              })
              encrypteparm.map(enc => {
                this.filter_data_variation.map(fil => {
                  if (fil.field_name == enc["variations.field_name"]) {
                    fil.child.map(chi => {
                      if (enc[fil.field_id].includes('OR')) {
                        let array = enc[fil.field_id].split('OR');
                        for (let i = 0; i < array.length; i++) {
                          if (chi.id.toString() == array[i].trim()) {
                            chi.is_checked = true;
                          }
                        }
                        this.changeStatus();
                      }
                    })
                  }
                })
              })
            }
            else {
              if (item.child.length > 0) {
                this.filter_data_non_variation.push(item);
                this.filter_data_non_variation.map(item => {
                  if (item.child.length > 0) {
                    item.child.map(x => {
                      x['is_checked'] = false;
                    })
                  }
                })
                encrypteparm.map(enc => {
                  this.filter_data_non_variation.map(fil => {
                    if (enc.hasOwnProperty(fil.field_id)) {
                      fil.child.map(chi => {
                        if (enc[fil.field_id].includes('OR')) {
                          let array = enc[fil.field_id].split('OR');
                          for (let i = 0; i < array.length; i++) {
                            if (chi.id.toString() == array[i].trim()) {
                              chi.is_checked = true;
                            }
                          }
                          this.changeStatus();
                        }
                      })
                    }
                  })
                })
              }
            }
            // let filter_set = this.elasticData();
            // console.log(filter_set);
            // this.showElasticDataInUI(filter_set);
            // console.log(item);
          }
        }
      })
    })
    this._globalService.showLoaderSpinner(false);
    
    // }
  }

  getPage(e) {
    window.scroll(0, 0);
    // console.log(e)
    this.p = e;
    let filter_set = this.elasticData();
    this.showElasticDataInUI(filter_set);
  }

  updateUrlImg(e,productData) {
    e.target.src = "/assets/images/noimg.png";
    productData['is_image_exists'] = false;
  }
  //breadcums
  getSubCategorydata(id, slug) {
    this.filter_data_non_variation = [];
    this.filter_price = [];
    this.category_id = id;
    let data: any;
    // this._route.queryParams.subscribe(params => {
    //   let value = JSON.parse((atob(params['search'])));
    //   value.id = id.toString();
    //   value.name = slug;
    //   data = btoa(JSON.stringify(value));
    // })

    // this.router.navigate(
    //   ['.'],
    //   {
    //     relativeTo: this._route, queryParams: { 'search': data }
    //   });
    // setTimeout(() => {
    //   this.ngOnInit();

    // }, 100);

  }

  changeStatus() {
    this.resetListing();
    this.filter_selected = [];
   /* this.filter_price.map(data => {
      if (data.child.length > 0) {
        data.child.map(x => {
          if (x.is_checked) {
            this.filter_selected.push(x);
          }
        })
      }
    })*/

    this.filter_data_non_variation.map(data => {

      if (data.child.length > 0) {

        data.child.map(x => {
          if (x.is_checked) {
            
            x['field_type'] = data['field_name'];
            
            this.filter_selected.push(x);
          }
        })
      }
    })

    this.filter_data_variation.map(data => {
      if (data.child.length > 0) {
        data.child.map(x => {
          if (x.is_checked) {
            x['field_type'] = data['field_name'];
            this.filter_selected.push(x);
          }
        })
      }
    })


    /*console.log("******************* Selected filter *******************");
    console.log(this.filter_selected);
    return false;*/
    let filter_set = this.elasticData();
    
    this.showElasticDataInUI(filter_set);
  }

  crossFilter(value) {
    this.resetListing();
    this.filter_data_non_variation.map(x => {
      if (x.child.length > 0) {
        x.child.map(y => {
          if (y.id == value.id) {
            y.is_checked = false;
          }
        })
      }
    });
    this.filter_selected = this.filter_selected.filter(item => item.id !== value.id);
    let filter_set = this.elasticData();
    this.showElasticDataInUI(filter_set);
  }


  clearAll() {
    this.resetListing();
    this.filter_selected = [];
    this.filter_data_non_variation.map(x => {
      if (x.child.length > 0) {
        x.child.map(y => {
          y.is_checked = false;
        })
      }
    });
    this.filter_price.map(x => {
      if (x.child.length > 0) {
        x.child.map(y => {
          y.is_checked = false;
        })
      }
    });
    this.filter_data_variation.map(x => {
      if (x.child.length > 0) {
        x.child.map(y => {
          y.is_checked = false;
        })
      }
    });
    let filter_set = this.elasticData();
    this.showElasticDataInUI(filter_set);
  }

  changeVariation(id, e) {
    let pro_list = this.product_list;
    this.product_list = [];
    let img: any;
    let price = [];
    let selected = ""
    pro_list.forEach(item => {

      if (item.id == id) {
        item.variation.forEach(data => {
          if (data.field_value == e) {
            data.product_images.forEach(im => {
              if (im.is_cover == 1) {
                img = im;
              }

            });
            price = (data.channel_currency_product_price);
            selected = data.field_value

          }
        })

        this.product_list.push({
          _id: item._id,
          amazon: item.amazon,
          asin: item.asin,
          amazon_addstatus: item.amazon_addstatus,
          avg_cost: item.avg_cost,
          barcode: item.barcode,
          best_selling: item.best_selling,
          brand: item.brand,
          category: item.category,
          channel_currency_product_price: this.formatChannelCurrencyProductPrice(price),
          default_price: item.default_price,
          description: item.description,
          hsn_id: item.hsn_id,
          id: item.id,
          name: item.name,
          product_images: img,
          is_image_exists :  true,
          sku: item.sku,
          slug: item.slug,
          unit: item.sku,
          weight : item.weight,
          uom : item.unit,
          url: item.sku,
          variation: item.variation,
          selected: selected

        });
      } else {
        this.product_list.push(item);
      }
    })

    // console.log(this.product_list)
    // console.log(this.selected)

    // else{
    //   alert("product is not in this category");
    //   this.router.navigate(['/']);
    // }



  }

  changesortvalue(e) {
    this.resetListing();
    let filter_set = this.elasticData(e);
    this.showElasticDataInUI(filter_set);
  }

  elasticData(sortingvalue?: any) {
    this.warehouse_id = this._globalService.getWareHouseId();
    //this.product_list = [];
    let urlModifiedCall = false;
    let value = "New Arrivals";
    let result = {};

    // if (sortingvalue) {
    switch (this.sorting_selected) {
      case "New Arrivals":
        result = {
          "created": {
            "order": "desc"
          }
        }
        break;
      case "Price : High to Low":
        result = {
          "channel_currency_product_price.new_default_price": {
            "order": "desc",
            "mode":  "avg",
            "nested_path" : "channel_currency_product_price",
            "nested_filter" : {
               "term" : {"channel_currency_product_price.warehouse_id" : this.warehouse_id}
            }
          }
        }

        break;
      case "Price : Low to High":
        result = {
          
          "channel_currency_product_price.new_default_price": {
            "order": "asc",
            "mode":  "avg",
            "nested_path" : "channel_currency_product_price",
            "nested_filter" : {
               "term" : {"channel_currency_product_price.warehouse_id" : this.warehouse_id}
            }
          }
        }
        break;
    }
    let first_filter = [];
    let second_filter = [];
    let third_filter = [];
    let query_range = [];
    first_filter.push({ "match": { "isdeleted": "n" } });
    first_filter.push({ "match": { "isblocked": "n" } });
    first_filter.push({ "match": { "visibility_id": { "query": "Catalog Search", "operator": "and" } } });
    let should_filter = {};
    let price_filter = [];
    let data = this.nonVariationValue();
    let price_value = this.priceQuery();
    let variation = this.variationvalue();
    if (data.length > 0) {
      data.map(x => {
        first_filter.push(x);
      })
      urlModifiedCall = true;
    }
    if (Object.keys(price_value).length > 0) {
     /* price_filter.push(price_value);
      urlModifiedCall = true;*/
      first_filter.push(price_value);
      urlModifiedCall = true;
    }
    if (variation.length > 0) {
      variation.map(x => {
        first_filter.push(x);
      })
      urlModifiedCall = true;
    }
    let from = 0;
   /* if (this.p <= 0 || this.p == undefined) {
      this.p = 1;
      from = 0;
    } else {
      let start = this.p - 1;
      from = start * this.page_size;
      //from = from - 1;
    }
    if (from < 0) {
      from = 0;
    }*/
    let must_filter = {};
    let must_not = {};

    let range_filter = {};
    let price_should_filter = {};
    
    third_filter.push({'nested' : {
            "path" : "inventory",
            "query" : {
                "bool" : {
                    "must" : [
                    { "term" : {"inventory.id" : this.warehouse_id} },
                    { "range" : {"inventory.stock" : {"gt" : 0}} }
                    ]
                }
            },
            "score_mode" : "avg"
      }
     },
     {
       'nested' : {
         "path" : "channel_currency_product_price",
         "query" : {
           "bool" : {
             "must" : [
               { 
                 "range": {
                  "channel_currency_product_price.new_default_price": {
                    "gt": 0,
             
                 }
               }
              },
              { "term": { "channel_currency_product_price.warehouse_id": this.warehouse_id } }
             ]
           }
         }
       }
     },
     {
       'nested' : {
         "path" : "product_images",
         "query" : {
           "bool" : {
             "must" : [
            
              { "term": { "product_images.is_cover": 1 } }
             ]
           }
         }
       }
     },
     {
       "terms" : {
         "id" : this.search_ids
       }
     }

    );
    
    must_filter['must'] = first_filter;
    should_filter['should'] = Object.keys(variation).length;
    price_should_filter['must'] = price_filter;

    range_filter["filter"] = third_filter;
    let final_value = {};
    

    if (second_filter.length > 0) {
      final_value = Object.assign(must_filter, (should_filter));

    }
    if (third_filter.length > 0) {
      final_value = Object.assign(must_filter, (range_filter));
    }
    if(price_filter.length > 0) {
      final_value = Object.assign(must_filter, (range_filter));
    }
    else {
      final_value = (must_filter);
    }
    final_value['must_not'] = {"term": {"product_images.img": ""}};
    let filter_set = {
      "query":
        { 
          "bool": final_value,
        },
        
      "from": this.from,
      "size": this.page_size,
      "sort": [
        result
      ]
    }
    // console.log(filter_set);
    /*if (urlModifiedCall) {
      this.routingUrlModified(first_filter);
    } if (!urlModifiedCall) {
      this.queryParamRemove();
    }*/
    // console.log(this.totalCount);
    return filter_set;
  }
  queryParamRemove() {
    if (this._route.snapshot.queryParams['search']) {
      this.router.navigate(
        ['.'],
        {
          relativeTo: this._route
        });
    }
  }

  showElasticDataInUI(filter_set) {
    this._globalService.showLoaderSpinner(true);
    this.global.getListingDataServer(filter_set).subscribe(data => {
      let pro_list;
      let selected = "";
      // console.log(data);
      if (data.hits.hits.length >= 1) {
        pro_list = data.hits.hits;
        this.pagination = {};
        this.variations_value = [];
        //let warehouse_id = "4";
        /*this.product_list = [];*/
        this.total_list = [];
        this.page_size = 18;//this._cookieService.getObject('globalData')['pagesize'] ? this._cookieService.getObject('globalData')['pagesize'] : 18;
        this.pagination.total_page = (Math.ceil(data.hits.total / this.page_size)).toString();
        this.config.currentPageCount = data.hits.total;
        this.config.currentPage = this.p;
        this.config.itemsPerPage = this.page_size;
        // this.all_product = data.hits.hits;
        for (let i = 0; i < data.hits.total; i++) {
          this.total_list.push(i);
        }
        // console.log(this.total_list)
        
        pro_list.forEach(item => {
          
          if (item._source.visibility_id == "Catalog Search") {
            if (item._source.inventory) {
              item._source.inventory.forEach(inven => {
                // && inven['stock'] > 0
                if (inven.id == this.warehouse_id) {
                  let stock = inven['stock'];
                  let img: any;
                  let variations = [];
                  if (item._source.product_images) {
                    item._source.product_images.forEach(im => {
                      if (im.is_cover == 1) {
                        img = im;
                      }
                    })
                  }

                  if (item._source.variations) {
                    item._source.variations.forEach(im => {
                      if (im.is_parent == "y") {
                        selected = im.field_value[0];
                      }
                      variations.push({
                        field_id: im.field_id,
                        field_label: im.field_label,
                        field_name: im.field_name,
                        field_value: im.field_value,
                        is_parent: im.is_parent,
                        field_show_value: im.field_value + " " + "- " + " ",
                        product_details: im.product_details,
                        channel_currency_product_price: this.formatChannelCurrencyProductPrice(im.product_details.channel_currency_product_price),
                        product_images: im.product_details.product_images,
                      })
                    })
                  }

                  this.product_list.push({
                    _id: item._id,
                    amazon: item._source.amazon,
                    asin: item._source.asin,
                    isblocked: item._source.isblocked,
                    isdeleted: item._source.isdeleted,
                    order_id: item._source.order_id,
                    status: item._source.status,
                    brand: item._source.brand,
                    category: item._source.category,
                    channel_currency_product_price: this.formatChannelCurrencyProductPrice(item._source.channel_currency_product_price),
                    default_price: item._source.default_price,
                    description: item._source.description,
                    hsn_id: item._source.hsn_id,
                    id: item._source.id,
                    name: item._source.name,
                    product_images: img,
                    is_image_exists :  true,
                    sku: item._source.sku,
                    slug: item._source.slug,
                    unit: item._source.sku,
                    weight : item._source.weight,
                    uom : item._source.unit,
                    veg_nonveg_type: item._source.veg_nonveg_type,
                    url: item._source.sku,
                    variation: variations,
                    selected: selected,
                    max_order_unit: item._source.max_order_unit,
                    IsCart: false,
                    quantity: item._source.quantity,
                    isSaveList:false,
                    stock : stock
                  });
               
                }
              })
            }
          }
      
        })
      } else {
        // this._globalService.showToast('Product is not available in this category');
      }
      this._globalService.showLoaderSpinner(false);
    })
    // console.log(this.product_list)
  }
  formatChannelCurrencyProductPrice(channelPrice = []) {
    let priceArray = [];
    let formattedArray = [];
    if(channelPrice && channelPrice.length > 0) {
      priceArray = channelPrice.filter(channelCurrencyProductPrice => {
        return channelCurrencyProductPrice['warehouse_id'] == this.warehouse_id;
      })
    }
    if(priceArray.length > 0) {
     formattedArray[0] = priceArray[0];
    }
    return formattedArray;
    


  }
  getDiscountPriceOrPercentage(channelCurrenctProductPrice) {
    let wareHouseId = this.warehouse_id;
    let selectedWareHousePriceData = [];
    selectedWareHousePriceData = channelCurrenctProductPrice.filter(priceData => {
      return priceData['warehouse_id'] == wareHouseId;
    })
    if(selectedWareHousePriceData.length > 0 && selectedWareHousePriceData[0]['discount_price'] > 0) {
      let discType = selectedWareHousePriceData[0]['disc_type'];
      let discountText = discType == 1 ?  selectedWareHousePriceData[0]['discount_amount']+'% OFF': 'AED '+selectedWareHousePriceData[0]['discount_amount']+' OFF';
      return discountText;
    }
    /*console.log("********************** Channel currency price *****************");
    console.log(selectedWareHousePriceData);*/
    return '';


  }

  addItem(item) {
    this.product_list.map(x => {
      if (x.id == item.id) {
        // if((x.quantity).toString() > x.max_order_unit.toString()){
        //   this._globalService.showToast("you can not oder more than"+x.max_order_unit+"items");
        // }else{
        x.quantity = x.quantity + 1;
        // }
      }
    });
    this.localStorage.setItem('product_list', JSON.stringify(this.product_list));
  }

  variationvalue() {
    let total_filter_data_variation = "";
    let first_filter;
    let final_item = {};
    let all_item = [];
    let resust = {}
    let field_val: any;
    // console.log("********************* Filter data variation **************************");
    // console.log(this.filter_data_variation);
    if (this.filter_data_variation.length > 0) {
      for (let i = 0; i < this.filter_data_variation.length; i++) {
        for (let j = 0; j < this.filter_data_variation[i]['child'].length; j++) {
          if (this.filter_data_variation[i]['child'][j].is_checked) {
            /*console.log("****************** Filter value child **************");
            console.log(this.filter_data_variation[i]['child'][j]);*/
            if (total_filter_data_variation != "") {
              /* alert(this.filter_data_variation[i]['child'][j].id);
               return false;*/
              total_filter_data_variation = total_filter_data_variation + "," + this.filter_data_variation[i]['child'][j]['name'];
            } else {
              //total_filter_data_variation =this.filter_data_variation[i].field_value;
              total_filter_data_variation = this.filter_data_variation[i]['child'][j]['name'];
            }
          }
          if (this.filter_data_variation[i]['child'].length - 1 == j && total_filter_data_variation != "") {
            all_item.push({ "match": { "custom_fields.field_name": { "query": this.filter_data_variation[i].field_id.toString(), "operator": "or" } } },
              { "match": { "custom_fields.value": { "query": total_filter_data_variation, "operator": "or" } } });

            // resust = Object.assign(resust, (field_val));
            // let field_name = 'variations.field_name :'+this.filter_data_variation[i].field_id.toString();
            // console.log(field_name);
            // // val=(total_brand);
            // let val = total_filter_data_variation.toString().split(',');
            // let qs = ''
            // for (let q = 0; q < val.length; q++) {
            //   if (qs) {
            //     qs += ' OR ' + val[q]
            //   } else {
            //     qs += val[q]
            //   }
            // }
            // final_item = {
            //   "query_string": {
            //     "fields": [
            //       field_name
            //     ],
            //     "query": qs
            //   }
            // }
            // all_item.push(final_item);
            // console.log(all_item)

            total_filter_data_variation = "";
            // console.log(first_filter);
            // console.log(total_filter_data_variation);
          }

        }
      }
    }
    return all_item;
  }

  nonVariationValue() {


    let total_brand = "";
    let first_filter;
    let final_item = {};
    let all_item = [];

    let category_id = [];
    let brand_id = [];
    let bran_slug = [];
    let exclude_types = ['categories','brand'];
    if (this.filter_data_non_variation.length > 0) {
      for (let i = 0; i < this.filter_data_non_variation.length; i++) {
        for (let j = 0; j < this.filter_data_non_variation[i]['child'].length; j++) {
          if (this.filter_data_non_variation[i]['child'][j].is_checked) {
            if (total_brand != "") {
              total_brand = total_brand + "," + this.filter_data_non_variation[i]['child'][j].slug;
            } else {
              total_brand = this.filter_data_non_variation[i]['child'][j].slug;
            }
            
          }
            if(this.filter_data_non_variation[i]['child'][j] && this.filter_data_non_variation[i]['child'][j]['is_checked']) {
             
               if(this.filter_data_non_variation[i]['child'][j]['field_type'] == 'categories') {
                 category_id.push(this.filter_data_non_variation[i]['child'][j]['id']);
               }
               if(this.filter_data_non_variation[i]['child'][j]['field_type'] == 'brand') {
                 brand_id.push(this.filter_data_non_variation[i]['child'][j]['id']);

               }

            }

          if (this.filter_data_non_variation[i]['child'].length - 1 == j && total_brand != "" && this.filter_data_non_variation[i]['child'][j]['is_checked'] && !exclude_types.includes(this.filter_data_non_variation[i]['child'][j]['field_type'])) {
   
            let field_name = this.filter_data_non_variation[i].field_id.toString();
            all_item.push({ "match": { [field_name]: { "query": total_brand, "operator": "or" } } });
            total_brand = "";
          
          }
        }
      }
      if(category_id.length > 0) {
         all_item.push({ "terms": {'category_id': category_id }});
      }
      if(brand_id.length > 0) {
        all_item.push({ "terms": {'brand_id': brand_id }});

      }

    }
    return all_item;
  }

  priceQuery() {
    let priceRangeFilter = {};
    let rangeQuery = {};
    /*console.log("***************************  Filter price ********************");
    console.log(this.filter_price);
    let priceRangeValue = {};*/
    if(this.selectedPriceRange && this.selectedPriceRange > 0) {
      rangeQuery['gt'] = 0;
      rangeQuery['lte'] = this.selectedPriceRange;
      priceRangeFilter['range'] = { "channel_currency_product_price.new_default_price": rangeQuery };
    }
    return priceRangeFilter;



    /*if (this.filter_price.length > 0) {
      for (let i = 0; i < this.filter_price.length; i++) {
        for (let j = 0; j < this.filter_price[i]['child'].length; j++) {

          if (this.filter_price[i]['child'][j].is_checked) {
            let rangeQuery = {};
            this.filter_price[i]['child'][j].min ? rangeQuery['gte'] = this.filter_price[i]['child'][j].min : '';
            this.filter_price[i]['child'][j].max ? rangeQuery['lte'] = this.filter_price[i]['child'][j].max : '';
            clicked_value.push({ "range": { "channel_currency_product_price.new_default_price": rangeQuery } })
            
            // clicked_value.push({ "range": { [this.filter_price[i].field_id]: { "gte": this.filter_price[i]['child'][j].min, "lte": this.filter_price[i]['child'][j].max } } })
          }

        }
      }
    }*/
    
  }

  routingUrlModified(first_filter) {
    let filter_value: any = {};
    this.pagination = {};
    this.variations_value = [];
    //let warehouse_id = "4";
    this.product_list = [];
    this.total_list = [];
    this.total_list = [];
    this.total_list = [];
    this.config = {};
    // this._route.queryParams.subscribe(params => {
    // let value = JSON.parse((atob(params['search'])));
    first_filter.map(data => {

      if (data.match) {
        if (!data.match['category_id'] && !data.match.isdeleted && !data.match.isblocked && !data.match.visibility_id && !data.match["inventory.id"]) {
          filter_value = Object.assign(filter_value, (data.match));
        }
      }

      if (data.query_string) {
        let field_name = data.query_string.fields[0];
        let field_value = data.query_string.query;
        let val = { [field_name]: field_value }
        filter_value = Object.assign(filter_value, val);
      }

     /* if (data.range) {
        let datamax = { maxvalue: data.range["channel_currency_product_price.new_default_price"].lte }
        let datamin = { minvalue: data.range["channel_currency_product_price.new_default_price"].gte }
        filter_value = Object.assign(
          filter_value, datamax);
        filter_value = Object.assign(
          filter_value, datamin);
      }*/
    }
    )
    // });
    let data = btoa(JSON.stringify(filter_value));
    // console.log("********************routingurl*******************");
    // console.log(filter_value);
    this.router.navigate(
      ['.'],
      {
        relativeTo: this._route, queryParams: { 'search': data }
      });
  }

  //  getting save list data after click on icon ....save-list
  getSaveList(product_id, add_new='n') {
    if(this.authenticationService.userFirstName) {
      let data= {
        "website_id":this._globalService.getFrontedWebsiteId()
      }
      if(add_new == 'n') {
        this.product_list.map(x => {
          if (x.id == product_id) {
            x.isSaveList = !x.isSaveList;
          } else {
            x.isSaveList = false;
          }
        });
      }

      this.global.getWebServiceData('save-list', 'GET', '', '').subscribe(data => {
        if (data.status == 1) {
          this.savelist_data = data.data;
          this.savelist_data.forEach(element => {
            var pro_ids=element.product_ids.replace (/"/g,'');
            if(pro_ids.includes(product_id)){
              element.is_checked=1;
            } else {
              // 
            }
          });
        } else {
          // console.log(data);
          this._globalService.showToast('Somthing wen\'t wrong. Please try again'); 
        }
      }, err => console.log(err), function() {});

    } else {
      if(!this.localStorage.getItem('currentUser')) {
        this._menuservice.signinSignuppopup$.next('sign-in');
        return false;
      }
    }
  }

  //  Add new save list ....save-list
  addNewSaveList(i:number, product_id, savelist_name = '') {
    if(this.authenticationService.userFirstName) {
      if(savelist_name == '') {
        this._globalService.showToast('Please enter savelist name'); 
      } else {
        let data= {
          "website_id":this._globalService.getFrontedWebsiteId(),
          "product_id":product_id,
          "name":savelist_name
        }
        this.global.getWebServiceData('save-list', 'POST', data, '').subscribe(data => {
        if (data.status == 200) {
          this.getSaveList(product_id, 'y');
          // this._globalService.showToast(data.message);
        } else {
          // console.log(data);
          this._globalService.showToast('Somthing wen\'t wrong. Please try again'); 
        }
        }, err => console.log(err), function() {});
      }
    } else {
      // this.openLoginDialog();
      if(!this.localStorage.getItem('currentUser')) {
        this._menuservice.signinSignuppopup$.next('sign-in');
        return false;
      }
    }
  }

  //  add and remove from save list....addremove-from-savelist
  addToSaveList(product_id:number, list_id:number, is_checked) {
    let action = 'add';
    if(is_checked) {
      action = 'del';
    }
    let post_data = {
      "website_id":this._globalService.getFrontedWebsiteId(),
      "product_id":product_id,
      "action": action,
      "list_id":list_id
    }
    if(this.authenticationService.userFirstName) {
      this.global.getWebServiceData('addremove-from-savelist', 'PUT', post_data, '').subscribe(data => {
      if (data.status == 200) {
        // this._globalService.showToast(data.message);
      } else {
        // console.log(data);
        this._globalService.showToast('Somthing wen\'t wrong. Please try again'); 
      }
      }, err => console.log(err), function() {});
    } else {
      // this.openLoginDialog();
      if(!this.localStorage.getItem('currentUser')) {
        this._menuservice.signinSignuppopup$.next('sign-in');
        return false;
      }
    }
  }

  //login dialog
  loginComponent: MatDialogRef<LoginComponent> | null;
  openLoginDialog() {
    this.loginComponent = this.dialog.open(LoginComponent, {
      disableClose: true
    });
  }

  sort_now(e:any=''){
    let el=this.sortBox.nativeElement as HTMLElement;
    el.classList.toggle('show');
    if(e==undefined || e=='' || e==null){
      //log
    }else{
      this.changesortvalue(e);
    }
  }
  cancel_sorting(){
    let el=this.sortBox.nativeElement as HTMLElement;
    el.classList.remove('show');
    this.sorting_selected="New Arrivals";
  }

  filter_now(e:any=''){
    let el=this.filterBox.nativeElement as HTMLElement;
    el.classList.add('show');
    this.set_subcat(this.filter_data_non_variation[0]);
  }
  filter_now_cancel(){
    let el=this.filterBox.nativeElement as HTMLElement;
    el.classList.remove('show');
    this.onChangePriceRangeValue(0);
    this.clearAll();
  }
  set_subcat(item:any){

    this.p = 0;
    this.subCat==null;
    if(item=='price_filter'){
      this.isPriceFilter=true
    }else{
      this.subCat=item.child;
      this.isPriceFilter=false
    }
    console.log(this.subCat);
  }
  set_brand(item:any){
    
    this.subBrand==null;
    this.subBrand=item.child;
  }                                                                                                                                     
  set_size(item:any){
    console.log(item);
    this.p = 0;
    this.subSize==null;
    this.subSize=item.child;
  }
  apply_filter(){
    let el=this.filterBox.nativeElement as HTMLElement;
    el.classList.toggle('show');
  }
  chnagePriceRangeSliderValue(value) {
    
    //this.changeStatus();
    return value;

  }
  onChangePriceRangeValue(value) {
    //console.log(event);
    // alert(value);
    this.selectedPriceRange = value;
    this.p = 0;
    this.changeStatus();

  }
  /**
   * Method for checking outof stock
   * @access public
  */
  checkIfProductIsOutOfStock(invenToryData) {
    console.log("************************ Inventory data ***********************");
    console.log(invenToryData);
    return true;


  }
   resetListing() {
    this.window.scroll(0, 0);
    this.p = 0;
    this.pagination = {};
    this.from = 0;
    this.product_list = [];

  }
  onScroll() {
    //alert("hiii");
    
    this.from = this.from+18;
    this.page_size = this.page_size;
    let filter_set = this.elasticData();
    this.showElasticDataInUI(filter_set);
    
  }

}