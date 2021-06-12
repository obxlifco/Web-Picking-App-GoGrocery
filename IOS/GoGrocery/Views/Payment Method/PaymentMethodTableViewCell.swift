//
//  PaymentMethodTableViewCell.swift
//  GoGrocery
//
//  Created by NAV63 on 20/07/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class PaymentMethodTableViewCell: UITableViewCell {

    @IBOutlet weak var lblTermsHeight: NSLayoutConstraint!
    @IBOutlet weak var lblTerms: UILabel!
    @IBOutlet weak var lblPaymentType: UILabel!
    @IBOutlet weak var imgImage: UIImageView!
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }
    
}
