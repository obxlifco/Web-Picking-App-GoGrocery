//
//  PromoCode.swift
//  GoGrocery
//
//  Created by Nav63 on 11/02/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class PromoCode: UIView {

    @IBOutlet weak var promoView: UIView!
    @IBOutlet weak var lblPromo: UILabel!
    @IBOutlet weak var txtPromo: UITextField!
    @IBOutlet weak var btnPrompApply: UIButton!
    @IBOutlet weak var btnDismissPromo: UIButton!
    
    @IBOutlet weak var btnCancel: UIButton!
}
var promoXib = PromoCode()
func requestPromoView(vc: UIViewController){
    
    promoXib.removeFromSuperview() // make it only once
    promoXib = Bundle.main.loadNibNamed("PromoCode", owner: vc, options: nil)?.first as! PromoCode
    promoXib.frame = CGRect(x:0, y: 0, width: UIScreen.main.bounds.size.width, height: UIScreen.main.bounds.size.height)
    promoXib.alpha = 0
    
    UIView.animate(withDuration: 0.5) {
        promoXib.alpha = 1
    }
    appdelegate.window?.addSubview(promoXib)
}
