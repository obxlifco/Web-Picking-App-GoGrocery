import { BrowserModule } from '@angular/platform-browser';
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
// import { DashboardComponent } from './dashboard/dashboard.component';

import { DashboardComponent } from './dashboard/dashboard.component';
import { HomeComponent } from './dashboard/pages/home/home.component';
import { CommonModule } from '@angular/common';
import { ReturnsComponent } from './dashboard/pages/returns/returns.component';
import { StocksComponent } from './dashboard/pages/stocks/stocks.component';
import { OrdersComponent } from './dashboard/pages/orders/orders.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatSidenavModule} from '@angular/material/sidenav';
import { TestComponent } from './test/test.component';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatCardModule } from '@angular/material/card';
import { MatMenuModule } from '@angular/material/menu';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { LayoutModule } from '@angular/cdk/layout';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatListModule } from '@angular/material/list';
import { FooterComponent } from './footer/footer.component';
import {ScrollingModule} from '@angular/cdk/scrolling';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import {MatRippleModule} from '@angular/material/core';
import { AddnewproductComponent } from './components/addnewproduct/addnewproduct.component';
import { MatDialogModule } from '@angular/material/dialog';
import { AddproductcategoryComponent } from './components/addproductcategory/addproductcategory.component';
import {MatButtonToggleModule} from '@angular/material/button-toggle';
import { HttpClientModule } from '@angular/common/http';
import { LoginComponent } from './user/login/login.component';
import {NgxWebstorageModule} from 'ngx-webstorage';
import { ToastrModule } from 'ngx-toastr';
import { NgxSpinnerModule } from "ngx-spinner";
import { NavbarComponent } from './components/navbar/navbar.component';
import { DatepipePipe } from './core/pipe/datepipe/datepipe.pipe';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';
import { MatTimepickerModule } from 'mat-timepicker';
import { MatFormFieldModule } from '@angular/material/form-field';
import {MatDividerModule} from '@angular/material/divider';
import { EditproductweightComponent } from './components/editproductweight/editproductweight.component';
import { MapmodalComponent } from './components/mapmodal/mapmodal.component';
import { SubcategoryComponent } from './components/subcategory/subcategory.component';
import { MatSelectFilterModule } from 'mat-select-filter';
import { SearchfilterPipe } from './core/pipe/searchfilter/searchfilter.pipe';
import { HighlightDirective } from './core/directive/highlight.directive';
import { NgxSkeletonLoaderModule } from 'ngx-skeleton-loader';
import { BillnumberComponent } from './components/billnumber/billnumber.component';
import {MatBadgeModule} from '@angular/material/badge';
import { ForgotpasswordComponent } from './user/login/forgotpassword/forgotpassword.component';
import { EditpriceComponent } from './components/editprice/editprice.component';
import {DatePipe} from '@angular/common';
import {MatSelectInfiniteScrollModule} from 'ng-mat-select-infinite-scroll';
import { MatSelectModule } from '@angular/material/select';
import { TimerpipePipe } from './timerpipe.pipe';
import { CountdownModule } from 'ngx-countdown';

@NgModule({
  declarations: [
    AppComponent,
    // DashboardComponent,
    DashboardComponent,   
    HomeComponent ,
    ReturnsComponent,
    StocksComponent,
    OrdersComponent,
    TestComponent,
    FooterComponent,
    AddnewproductComponent,
    AddproductcategoryComponent,
    LoginComponent,
    NavbarComponent,
    DatepipePipe,
    EditproductweightComponent,
    MapmodalComponent,
    SubcategoryComponent,
    SearchfilterPipe,
    HighlightDirective,
    BillnumberComponent,
    ForgotpasswordComponent,
    EditpriceComponent,
    TimerpipePipe 
  ],
  imports: [
    BrowserModule,
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    AppRoutingModule,
    NgxWebstorageModule.forRoot(),
    BrowserAnimationsModule,
    MatSidenavModule,
    MatGridListModule,
    ToastrModule.forRoot(),
    MatCardModule,
    MatMenuModule,
    MatIconModule,
    MatButtonModule,
    LayoutModule,
    MatToolbarModule,
    MatListModule,
    MatRippleModule,
    ScrollingModule,
    MatDialogModule,
    MatButtonToggleModule,
    HttpClientModule,
    NgxSpinnerModule ,
    MatSlideToggleModule,
    MatTimepickerModule,
    MatFormFieldModule,
    MatDividerModule,
    MatSelectFilterModule,
    NgxSkeletonLoaderModule,
    MatBadgeModule,
    MatSelectInfiniteScrollModule,
    MatSelectModule,
    CountdownModule
  ],
  providers: [
    DatePipe
  ],
  schemas:  [ CUSTOM_ELEMENTS_SCHEMA ],
  bootstrap: [AppComponent]
})
export class AppModule { }
