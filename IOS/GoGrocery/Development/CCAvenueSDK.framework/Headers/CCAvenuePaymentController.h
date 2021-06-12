//
//  CCAvenuePaymentController.h
//  SeamlessKitUAE
//
//  Created by Mayur Shinde on 12/11/18.
//  Copyright © 2018 Avenues. All rights reserved.
//

#import <UIKit/UIKit.h>

@class CCUICheckbox;

@class CCAvenuePaymentController;

@protocol CCAvenuePaymentControllerDelegate <NSObject>

-(void)getResponse:(NSMutableDictionary *)responseDict_;

@end

@interface CCAvenuePaymentController : UIViewController

- (id)initWithOrderId:(NSString *)orderId_ merchantId:(NSString *)merchantId_ accessCode:(NSString *)accessCode_ custId:(NSString *)custId_ amount:(NSString *)amount_ currency:(NSString *)currency_ rsaKeyUrl:(NSString *)rsaKeyUrl_ redirectUrl:(NSString *)redirectUrl_ cancelUrl:(NSString *)cancelUrl_ showAddress:(NSString *)showAddress_ billingName:(NSString *)billingName_ billingAddress:(NSString *)billingAddress_ billingCity:(NSString *)billingCity_ billingState:(NSString *)billingState_ billingCountry:(NSString *)billingCountry_  billingTel:(NSString *)billingTel_ billingEmail:(NSString *)billingEmail_ deliveryName:(NSString *)deliveryName_ deliveryAddress:(NSString *)deliveryAddress_ deliveryCity:(NSString *)deliveryCity_ deliveryState:(NSString *)deliveryState_ deliveryCountry:(NSString *)deliveryCountry_ deliveryTel:(NSString *)deliveryTel_ promoCode:(NSString *)promoCode_ merchant_param1:(NSString *)merchant_param1_ merchant_param2:(NSString *)merchant_param2_ merchant_param3:(NSString *)merchant_param3_ merchant_param4:(NSString *)merchant_param4_ merchant_param5:(NSString *)merchant_param5_ useCCPromo:(NSString *)useCCPromo_;

@property (nonatomic, weak) id<CCAvenuePaymentControllerDelegate> delegate;

@property(nonatomic, retain)IBOutlet CCUICheckbox *saveCardCheckbox;

@end
