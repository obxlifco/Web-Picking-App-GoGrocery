import UIKit
class OrderItemTableViewCell: UITableViewCell {

    @IBOutlet weak var itemNameLabel: UILabel!
    @IBOutlet weak var itemAmountLabel: UILabel!
    @IBOutlet weak var itemImageView: UIImageView!
     @IBOutlet weak var lblStock: UILabel!
    @IBOutlet weak var lblUnitItem: UILabel!
     @IBOutlet weak var lblUnitPrice: UILabel!
      @IBOutlet weak var lblOutOfStockHeight: NSLayoutConstraint!
     @IBOutlet weak var lblStrike: UILabel!
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
