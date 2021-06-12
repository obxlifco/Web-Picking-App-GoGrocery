import { Component, AfterViewInit, OnInit, OnDestroy} from '@angular/core';
import { Http } from '@angular/http';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie';
import { Global } from '../global/service/global';
import { GlobalService } from '../global/service/app.global.service';
import { ChartOptions } from 'chart.js';
import { Color} from 'ng2-charts';
import * as pluginAnnotations from 'chartjs-plugin-annotation';
import * as moment from 'moment';
import { DashboardService } from './dashboard.service';

@Component({
  selector: 'my-app',
  providers: [DashboardService, Global],  
  templateUrl: './templates/dashboard.component.html'
})
export class DashboardComponent implements OnInit,OnDestroy {
  public response: any;
  public errorMsg: string;
  public successMsg: string;  
  public formModel: any = {};
  private sub: any;
  public tabIndex: number;
  public parentId: number = 0;
  public ipaddress: any;
  public top_customers: any;
  public top_sold_products:any;
  public most_viewed_pages:any;
  public new_customer:any;
  public diff_in_percent:any;
  public invoice_nos :any;
  public invoice_percent:any;
  public percent_of_new_visit:any;
  public avg_time_on_site:any;
  public page_view:any;
  public warehouse_list: any = []; 
  public default_warehouse: number =0;
  public customerBarChartData:any;
  public new_visitors    :any;
  public site_visit      :any;
  public unique_visitor  :any;
  
  public total_sales     :any;
  public sales_percent   :any;
 
  public doughnutChartLabelsVisitor = ['Mobile Store','POS'];
  public doughnutChartDataVisitor: number[] = [];
  public doughnutChartTypeVisitor: string = 'doughnut';
  public selectedStartDate:any;
  public selectedEndDate:any;
  public selectedItem :string = 'day';
  public graphdata:any;
  public graphlable:any;
  public userData:any={};
  public storeReport:any = [];
  public colors = [{
      backgroundColor: [
          'rgb(184, 4, 89)',
          'rgb(247, 158, 149)',
          'rgb(122, 196, 89)',
          'rgb(247, 3, 116)',
          'rgb(26, 47, 116)',
          'rgb(125, 4, 89)'
      ]
  }];
 

  
  public selected: any;
  alwaysShowCalendars: boolean;
  showRangeLabelOnInput: boolean;
  keepCalendarOpeningWithRange: boolean;
  maxDate: moment.Moment;
  minDate: moment.Moment;
  invalidDates: moment.Moment[] = [moment().add(2, 'days'), moment().add(3, 'days'), moment().add(5, 'days')];
  ranges: any = {
      'Today': [moment(), moment()],
      'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
      'Last 7 Days': [moment().subtract(6, 'days'), moment()],
      'Last 30 Days': [moment().subtract(29, 'days'), moment()],
      'This Month': [moment().startOf('month'), moment().endOf('month')],
      'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
  }
  
  //sales graph//
  public ChartDataSets: any = [];
  public lineChartData: any = [];
  public chart_data: any = [];
  public chart_label: string = ''; 
  public graph_lables:any =[];
  public report_type: string = '';
  public chart_yAxisID: string = '';
  public lineChartLabels:any = [''];
  public lineChartOptions: (ChartOptions & { annotation: any }) = {
    responsive: true,   
    annotation: {
      annotations: [
        {
          type: 'line',
          mode: 'vertical',
          scaleID: 'x-axis-0',
          value: 'March',
          borderColor: 'orange',
          borderWidth: 2,
          label: {
            enabled: true,
            fontColor: 'orange',
            content: 'LineAnno'
          }
        },
      ],
    },
  };
  public lineChartColors: Color[] = [
    { // grey
      backgroundColor: 'rgba(148,159,177,0.2)',
      borderColor: 'rgba(148,159,177,1)',
      pointBackgroundColor: 'rgba(148,159,177,1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(148,159,177,0.8)'
    }
  ];
  public lineChartLegend = true;
  public lineChartType = 'line';
  public lineChartPlugins = [pluginAnnotations];
  //end sales graph//  
  constructor(
    private _dashboardService: DashboardService,
    private _router: Router,
    private _cookieService:CookieService,
    public _globalService: GlobalService
  ) {
    this.ipaddress = _globalService.getCookie('ipaddress');
    this.maxDate = moment().add(2, 'weeks');
    this.minDate = moment().subtract(3, 'days');
    this.alwaysShowCalendars = true;
    this.keepCalendarOpeningWithRange = true;
    this.showRangeLabelOnInput = true;
    this.selected = {
        startDate: moment().subtract(30, 'days'),
        endDate: moment().subtract(0, 'days')
    };
  }
  ngOnInit() {
    var data: any = {};   
    this.report_type       = "day";
    this.chart_label       = "Sales"; 
    this.selectedStartDate = this._globalService.convertDate(moment().subtract(30, 'days'), 'yyyy-MM-dd');
    this.selectedEndDate   = this._globalService.convertDate(moment().subtract(0, 'days'), 'yyyy-MM-dd');
    this.selectedItem      = 'day';
    data.website_id        = this._globalService.getWebsiteId();
    data.company_id        = 1;    
    data.start_date        = this.selectedStartDate;
    data.end_date          = this.selectedEndDate;   
    data.report_type       = this.report_type
    data.chart_label       = this.chart_label
    data.warehouse_id      = this.default_warehouse;
    // "report_type":"week/month/day/year"    
    this.getWarehouselist();
    this.getDashboardDetails(data);
    this.getGraphdetails(data);
   
    // this.lineChartData.push({
    //   data: this.chart_data, 
    //   label: this.chart_label,
    //   yAxisID: this.chart_yAxisID
    // }) 
   
    
    // Onchnage website id
    this._globalService.chnageWebSite$.subscribe(response => {
      if(response) {
        this.selectedItem      = 'day';
        this.resetgraphdata();        
        this.getDashboardDetails(data);
        this.getGraphdetails(data);
        this.getWarehouselist();
      }
    });

    this._globalService.changedaterange$.subscribe(response => {
      if(response) {
        data.website_id = this._globalService.getWebsiteId();
        this.getDashboardDetails(data);
        this.getGraphdetails(data);
      }
    });
    this.userData = this._cookieService.getObject('userData');
  }
  getWarehouselist(){
    let obj = {};
		obj["id"]= 0;
		obj["name"]='All Store';
    var data: any = {};
    let websiteId = this._globalService.getWebsiteId();
    this._dashboardService.warehouseLoad(websiteId).subscribe(
        data1 => {
            this.warehouse_list = data1.warehouse;
            console.log(this.userData['user_type'])
            if(this.userData['user_type']=='SuperAdmin'){
              this.warehouse_list.splice(0, 0, obj);
            }
            console.log(this.warehouse_list)
            // this.default_warehouse = 0;
            data.warehouse_id = this.default_warehouse;
        },
        err => console.log(err),
        function() {
            //completed callback
        }
    );
  }
  callbackLoaddashboard(warehouse_id: number){   
    this.default_warehouse = warehouse_id;
    var data: any     = {};     
    data.website_id   = this._globalService.getWebsiteId();
    data.company_id   = 1;
    data.warehouse_id = this.default_warehouse;  
    data.report_type  = this.report_type
    if(this.selectedStartDate != null){
      data.start_date = this.selectedStartDate;
      data.end_date   = this.selectedEndDate;
    }else{
      data.start_date = this._globalService.convertDate(moment().subtract(30, 'days'), 'yyyy-MM-dd');
      data.end_date   = this._globalService.convertDate(moment().subtract(0, 'days'), 'yyyy-MM-dd');
    }  
    this.resetgraphdata(); 
    this.getDashboardDetails(data);
    this.getGraphdetails(data);
  }
  getDashboardDetails(data) {
      this._dashboardService.dashboardLoad(data).subscribe(data => {
      this.response           =   data;   

      this.storeReport =this.response;
      console.log(this.storeReport)
         
      // this.top_customers      =   this.response.top_customers;  
      // this.top_sold_products  =   this.response.top_sold_products;
      // this.most_viewed_pages  =   this.response.most_viewed_pages; 
      // let diff_in_percent     =   this.response.new_customers.diff_in_percent;
      // this.new_customer       =   this.response.new_customers.new_customer.toLocaleString();
      // this.diff_in_percent    =   diff_in_percent.toFixed(2);

      // this.invoice_nos        =   this.response.new_invoice.new_invoice.toLocaleString();
      // let invoice_percent     =   this.response.new_invoice.diff_in_percent;
      // this.invoice_percent    =   invoice_percent.toFixed(2);

      // this.new_visitors       =   this.response.traffic_report.new_visitors;
      // this.site_visit         =   this.response.traffic_report.site_visit;
      // this.unique_visitor     =   this.response.traffic_report.unique_visitor;
      // this.percent_of_new_visit     =   this.response.traffic_report.percent_of_new_visit.toFixed(2);
      // this.avg_time_on_site         =   this.response.traffic_report.avg_time_on_site.toFixed(2);
      // this.page_view                =   parseInt(this.response.traffic_report.page_view);
      

      // this.total_sales        =   this.response.new_sales_monthly.total_order_today.toLocaleString();
      // this.sales_percent      =   this.response.new_sales_monthly.diff_in_percent.toFixed(2);

      
      
      // let channel_wisw_data   =  this.response.marketplace_report.channel_wisw_data;      

      // var marketplace_data:any=[];
      // var channel_name:any=[];

      // channel_wisw_data.forEach(function(item:any){        
      //     marketplace_data.push(parseFloat(item.sales_percent.toFixed(2)));       
      // });

      // channel_wisw_data.forEach(function(item:any){        
      //   channel_name.push(item.channel_name);       
      // });    
      // // console.log(channel_name);
      // // console.log(this.doughnutChartLabelsVisitor);
     
      // this.doughnutChartLabelsVisitor = channel_name;
      // this.doughnutChartDataVisitor   = marketplace_data;
     
      }, err => {
          this._globalService.showToast('Something went wrong. Please try again.');
      }, function() {
          //completed callback
      });   
  }
 
  getGraphdetails(data){
    this._dashboardService.graphLoad(data).subscribe(data => {
      this.response   = data;
      let graph_lable = this.response.order_graph.data;   
      let graph_data  = this.response.order_graph.value;      
      //graph value//
      let that =this;     
      graph_data.forEach(item => {        
        that.chart_data.push(item.toFixed(2));
      });       
      //graph data      
      graph_lable.forEach(items => { 
        if( this.report_type == 'day' ||  this.report_type == 'week'){
          that.graph_lables.push(this._globalService.convertDate(items, 'd MMM'));  
        }else{
          that.graph_lables.push(items);
        }     
        
      }); 

      this.chart_label    = 'Sales';
      this.chart_yAxisID  = 'y-axis-0';
      this.lineChartLabels = this.graph_lables;
      this.customerBarChartData =true;
      this.lineChartData.push({
        data: this.chart_data, 
        label: this.chart_label,
        yAxisID: this.chart_yAxisID
      })   
      //end graph data//
      }, err => {
          this._globalService.showToast('Something went wrong. Please try again.');
      }, function() {
          //completed callback
      });
  }

  getgraphdata(type:any){    
    var data: any     = {};  
    this.report_type  = type;  
    this.selectedItem = type; 
    data.website_id   = this._globalService.getWebsiteId();
    data.company_id   = 1;
    data.warehouse_id = this.default_warehouse; 
    data.report_type  =  this.report_type;     
    if(this.selectedStartDate != null){
      data.start_date = this.selectedStartDate;
      data.end_date   = this.selectedEndDate;
    }else{
      data.start_date = this._globalService.convertDate(moment().subtract(30, 'days'), 'yyyy-MM-dd');
      data.end_date   = this._globalService.convertDate(moment().subtract(0, 'days'), 'yyyy-MM-dd');
    }      
    this.resetgraphdata();
     
    this.getGraphdetails(data);
  }

  

  datesUpdatedApply(range) {    
    this.AppplyDate(range, 'n');
  }

  AppplyDate(range, load_first: any='n') {    
    const myObjStr = JSON.stringify(range);
    const selected_dates = JSON.parse(myObjStr);   
    this.selectedStartDate = this._globalService.convertDate(selected_dates.startDate, 'yyyy-MM-dd');    
    this.selectedEndDate = this._globalService.convertDate(selected_dates.endDate, 'yyyy-MM-dd'); 
    var data: any = {};
    data.website_id = this._globalService.getWebsiteId();
    data.company_id = 1;
    data.start_date = this.selectedStartDate;
    data.end_date   = this.selectedEndDate;
    data.report_type= this.report_type;
    data.warehouse_id=this.default_warehouse;
    this.resetgraphdata();
    if (this.selectedStartDate != null && this.selectedEndDate != null && load_first != 'y') {
        this.getDashboardDetails(data);
        this.getGraphdetails(data);
    }
    
  }

  resetgraphdata(){
    this.chart_data = [];                
    this.chart_label    = '';
    this.chart_yAxisID  = 'y-axis-0';
    this.lineChartLabels = '';
    this.lineChartData = []; 
    this.graph_lables = []; 
  }

  ngOnDestroy() {
    // this.sub.unsubscribe();
  } 

   // events on slice click
   public chartClicked(e:any):void {
    console.log(e);
  }
 
 // event on pie chart slice hover
  public chartHovered(e:any):void {
    console.log(e);
  }

  loadStoreWiseOrder(menuId:number,status) {
    this._cookieService.putObject('warehouse_status', status);
    if(menuId  == 77) {
      this._router.navigate(['/orders']);
    } else {
      this._router.navigate(['/shipment/shipment']);
    }    
  }
}
