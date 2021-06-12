import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { DashboardRoutingModule } from './dashboard-routing.module';
import { DashboardComponent } from './dashboard.component';
import { ChartsModule } from 'ng2-charts';
import { BmscommonModule } from '../bmscommon.module';
import { NgxDaterangepickerMd } from 'ngx-daterangepicker-material';

// Import angular-fusioncharts
import { FusionChartsModule } from 'angular-fusioncharts';

// Import FusionCharts library
import * as FusionCharts from 'fusioncharts';

// Load FusionCharts Individual Charts
import * as Charts from 'fusioncharts/fusioncharts.charts';
import * as FusionTheme from 'fusioncharts/themes/fusioncharts.theme.fusion';
import { NgSelectModule } from '@ng-select/ng-select';
FusionChartsModule.fcRoot(FusionCharts, Charts,FusionTheme)

@NgModule({
  declarations: [DashboardComponent],
  imports: [
    CommonModule,
    DashboardRoutingModule,
    BmscommonModule,  
    ChartsModule,
    FusionChartsModule,
    NgxDaterangepickerMd,
    FusionChartsModule,
    NgSelectModule
  ]
})
export class DashboardModule { }
