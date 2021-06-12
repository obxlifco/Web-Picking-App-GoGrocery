import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
/*import { AuthGuardEditor,AuthGuard, AuthGuardMerchant } from './global/service/auth-guard.service';
import { GlobalVariable } from './global/service/global';
import { PageComponent } from './pages/app.page.component';
import { ViewPageBuilderComponent } from './cms/view-page-builder.component';*/
/*import { DeliveryAddressComponent,WishlistComponent,ReviewsComponent,ChangePasswordComponent,UpdateProfileComponent,
        TrackOrdersComponent ,TicketComponent,TicketDetailsComponent } from './profile/app.profile.component';*/

// Modified code for lazy loading
import {CONTENT_ROUTES} from './global/routes/content-layout.routes';
import {UiComponent} from './ui/ui.component';
import { PromotionComponent } from './promotion/promotion.component';


const routes:Routes = [
    {
        path : '',
        data: { title: 'Home', is_cms: 0},
        component: UiComponent,
        children : CONTENT_ROUTES
    },
    {path : 'promotion',component:PromotionComponent},
    {
    	path : 'editor',
    	data: { title: 'Editor', is_cms: 1},
    	loadChildren : './modules/view-page-builder/view-page-builder.module#ViewPageBuilderModule',
    },
    
    { path: '**', redirectTo : 'not-found',pathMatch:'full' },

]

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }