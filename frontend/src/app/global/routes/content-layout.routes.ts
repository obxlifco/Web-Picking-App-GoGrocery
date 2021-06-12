import {Routes} from '@angular/router';
import { AuthGuardEditor, AuthGuardMerchant } from '../../global/service/auth-guard.service';
import { LoginComponent } from '../../login/login.component';
import {SuccesspaymentComponent} from '../../modules/successpayment/successpayment.component';
import {FailepaymentComponent} from '../../modules/failepayment/failepayment.component';
import {CancelpaymentComponent} from '../../modules/cancelpayment/cancelpayment.component';
import { AuthGuard } from '../../core/guards/auth.guard';
import { ContactusComponent } from '../../contactus/contactus.component';
import { MobileLandingComponent } from '../../mobile-landing/mobilelanding.component';
import { PromotionComponent } from '../../promotion/promotion.component';
import { SubstituteProductComponent } from '../../modules/substitute_product/substitute_product.component';
import { SuccessSubstituteComponent } from '../../modules/substitute_product/successSubstituteProduct/successSubstitute.component';




export const CONTENT_ROUTES:Routes = [
		{path : '',loadChildren:'./modules/home/home.module#HomeModule'},
		{path: 'home',loadChildren:'./modules/home/home.module#HomeModule'},
		{path : 'page/:slug',loadChildren : './modules/page/page.module#PageModule'},
		{path : 'not-found',loadChildren:'./modules/not-found/not-found.module#NotFoundModule'},
		{path : 'sign-up',loadChildren:'./modules/registration/registration.module#RegistrationModule'},
		{path : 'listing',loadChildren:'./modules/listing/listing.module#ListingModule'},
		{path : 'search',loadChildren : './modules/search/search.module#SearchModule'},
		{path : 'details/:slug',loadChildren : './modules/details/details.module#DetailsModule'},
		{path : 'cart',loadChildren : './modules/cart/cart.module#CartModule'},
		{path : 'checkout',canActivateChild:[AuthGuard],loadChildren:'./modules/checkout/checkout.module#CheckoutModule'},
		{ path: 'login', component: LoginComponent, data: { title: 'Login' } },
		{path : 'profile',canActivateChild:[AuthGuard],loadChildren:'./modules/profile/orderhistory/orderhistory.module#OrderhistoryModule'},
		{path : 'approved-order',loadChildren:'./modules/profile/orderhistory/orderhistory.module#OrderhistoryModule'},
		{path : 'reset-password/:id',loadChildren:'./modules/reset-password/reset-password.module#ResetPasswordModule'},
		{path : 'success-payment/:id',component:SuccesspaymentComponent},
		{path : 'failed-payment/:id/:status/:message',component:FailepaymentComponent},
		{path : 'contact-us',component:ContactusComponent},
		{path : 'landing',component:MobileLandingComponent},
		{path : 'substitute-product/:slug',loadChildren : './modules/substitute_product/substitute_product.module#SubstituteProductModule'},
		{path : 'success-substitute/:id',component : SuccessSubstituteComponent}

		
	]
									
									
	// {path : 'login',loadChildren:'./modules/login/login.module#LoginModule'},
	// {path : 'login',loadChildren:'./modules/login/login.module#LoginModule'},