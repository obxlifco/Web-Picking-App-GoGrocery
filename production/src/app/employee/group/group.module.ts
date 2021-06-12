import { NgModule } from '@angular/core';
import { BmscommonModule } from '../../bmscommon.module';
import { CommonModule } from '@angular/common';
import { GroupRoutingModule } from './group-routing.module';
import { GroupComponent }  from '../../employee/group/employee.group.component';
import { GroupAddEditComponent }  from '../../employee/group/employee.group.addedit.component';
import { NgSelectModule } from '@ng-select/ng-select';

@NgModule({
  declarations: [
  	GroupComponent,
  	GroupAddEditComponent,
  ],
  imports: [
    CommonModule,
    GroupRoutingModule,
    BmscommonModule,
    NgSelectModule
  ]
})
export class GroupModule { }
