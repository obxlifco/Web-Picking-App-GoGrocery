import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BmscommonModule } from '../../bmscommon.module';

import { RoleRoutingModule } from './role-routing.module';

import { RoleComponent }  from '../../employee/role/employee.role.component';
import { RoleAddEditComponent }  from '../../employee/role/employee.role.addedit.component';
import { NgSelectModule } from '@ng-select/ng-select';

@NgModule({
  declarations: [
  	RoleComponent,
  	RoleAddEditComponent,
  ],
  imports: [
    CommonModule,
    RoleRoutingModule,
    BmscommonModule,
    NgSelectModule
  ]
})
export class RoleModule { }
