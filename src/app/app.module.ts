import { BrowserModule } from '@angular/platform-browser';
import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { HomeComponent } from './dashboard/pages/home/home.component';
import { CommonModule } from '@angular/common';
import { ReturnsComponent } from './dashboard/pages/returns/returns.component';
import { StocksComponent } from './dashboard/pages/stocks/stocks.component';
import { OrdersComponent } from './dashboard/pages/orders/orders.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatSidenavModule} from '@angular/material/sidenav';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatCardModule } from '@angular/material/card';
import { MatMenuModule } from '@angular/material/menu';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { LayoutModule } from '@angular/cdk/layout';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatListModule } from '@angular/material/list';
import {ScrollingModule} from '@angular/cdk/scrolling';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import {MatNativeDateModule, MatRippleModule} from '@angular/material/core';
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
import { CountdownModule } from 'ngx-countdown';
import { AddproductasSubtituteComponent } from './components/addproductas-subtitute/addproductas-subtitute.component';
import { EmptystateComponent } from './components/emptystate/emptystate.component';
import { AppsettingsComponent } from './components/appsettings/appsettings.component';
import {MatCheckboxModule} from '@angular/material/checkbox';
import { MessagedialogComponent } from './components/messagedialog/messagedialog.component';
import { InfiniteScrollModule } from 'ngx-infinite-scroll';
import { SalesreportComponent } from './dashboard/pages/salesreport/salesreport.component';
import {MatDatepickerModule} from '@angular/material/datepicker';
import { NotfoundComponent } from './components/notfound/notfound.component';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatTabsModule} from '@angular/material/tabs';
import { TestComponent } from './test/test.component';
import { UiSwitchModule } from 'ngx-ui-switch';
import {MatTooltipModule} from '@angular/material/tooltip';
import { ImagemagnifyComponent } from './components/imagemagnify/imagemagnify.component';
import { MatInputModule } from '@angular/material/input';
import { ProductimportComponent } from './components/productimport/productimport.component';
import { BulkproductdataComponent } from './components/bulkproductdata/bulkproductdata.component';
import { NgxFileDropModule } from 'ngx-file-drop';

@NgModule({
  declarations: [
    AppComponent,
    // DashboardComponent,
    DashboardComponent,   
    HomeComponent ,
    ReturnsComponent,
    StocksComponent,
    OrdersComponent,
    AddnewproductComponent,
    AddproductcategoryComponent,
    LoginComponent,
    NavbarComponent,
    DatepipePipe,
    EditproductweightComponent,
    MapmodalComponent,
    SearchfilterPipe,
    HighlightDirective,
    BillnumberComponent,
    ForgotpasswordComponent,
    EditpriceComponent,
    AddproductasSubtituteComponent,
    EmptystateComponent,
    AppsettingsComponent,
    MessagedialogComponent,
    SalesreportComponent,
    NotfoundComponent,
    TestComponent,
    ImagemagnifyComponent,
    ProductimportComponent,
    BulkproductdataComponent 
  ],
  imports: [
    BrowserModule,
    CommonModule,
    FormsModule,
    InfiniteScrollModule,
    ReactiveFormsModule,
    AppRoutingModule,
    // AngularFireModule.initializeApp(environment.firebaseConfig),
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
    CountdownModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatCheckboxModule,
    MatExpansionModule,
    MatTabsModule,
    UiSwitchModule,
    MatTooltipModule,
    MatInputModule,
    NgxFileDropModule
    // fs
    // MatMomentDateModule
  ],
  providers: [
    DatePipe
  ],
  schemas:  [ CUSTOM_ELEMENTS_SCHEMA ],
  bootstrap: [AppComponent]
})
export class AppModule { }
