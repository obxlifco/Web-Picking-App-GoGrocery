//
//  OrderDetailsTableViewCell.swift
//  GoGrocery
//
//  Created by Nav121 on 06/02/20.
//  Copyright © 2020 BMS-09-M. All rights reserved.
//

import UIKit

class OrderDetailsTableViewCell: UITableViewCell {

    @IBOutlet weak var orderNoLabel: UILabel!
    @IBOutlet weak var orderDatelabel: UILabel!
    @IBOutlet weak var shippingNameLabel: UILabel!
    @IBOutlet weak var shippingAddress1Label: UILabel!
    @IBOutlet weak var shippingAddress2Label: UILabel!
    @IBOutlet weak var shippingMobileNoLabel: UILabel!
    
    @IBOutlet weak var subtotalLabel: UILabel!
    @IBOutlet weak var discountlabel: UILabel!
    @IBOutlet weak var deliverylabel: UILabel!
    @IBOutlet weak var totalAmtLabel: UILabel!
    
    @IBOutlet weak var lblNote: UILabel!
     @IBOutlet weak var lblNoteDes: UILabel!
    @IBOutlet weak var heightCardView: NSLayoutConstraint!
    @IBOutlet weak var heightLblNote: NSLayoutConstraint!
    @IBOutlet weak var heightLblNoteDes: NSLayoutConstraint!
    
    
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
