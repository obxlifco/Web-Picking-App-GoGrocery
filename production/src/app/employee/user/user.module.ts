import { NgModule } from '@angular/core';
import { BmscommonModule } from '../../bmscommon.module';
import { CommonModule } from '@angular/common';

import { UserRoutingModule } from './user-routing.module';
import { UserComponent }  from '../../employee/user/employee.user.component';
import { UserAddEditComponent }  from '../../employee/user/employee.user.addedit.component'; 
import { NgSelectModule } from '@ng-select/ng-select';
@NgModule({
  declarations: [
  	UserComponent,
  	UserAddEditComponent
  ],
  imports: [
    CommonModule,
    UserRoutingModule,
    BmscommonModule,
    NgSelectModule
  ]
})
export class UserModule { }
