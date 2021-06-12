
import UIKit
import TagListView
import SwiftyJSON
import FirebaseAnalytics
class SearchViewController: UIViewController ,TagListViewDelegate , UITextFieldDelegate ,MicSelectDelegate {
    
    // MARK: - Outlet declaration
    // MARK: -
    @IBOutlet weak var txtSearch: UITextField!
    @IBOutlet weak var collectionView: UICollectionView!
    @IBOutlet weak var tableView: UITableView!
    @IBOutlet weak var btnBackAction: UIButton!
    @IBOutlet weak var tagViewHeight: NSLayoutConstraint!
    @IBOutlet weak var tagView: TagsView!
    @IBOutlet weak var viewRecentHeight: NSLayoutConstraint!
    @IBOutlet weak var viewRecent: UIView!
    @IBOutlet weak var noProductView: UIView!
    @IBOutlet weak var btnVoiceSerach: UIButton!
    // MARK: - Variable declaration
    // MARK: -
    var titles = [JSON]()
    let wareHouseId = UserDefaults.standard.value(forKey: "WareHouseId") as! Int
    var queryString: String = ""
    var recentArr = [String]()
    var mustArray = [[String:Any]]()
    var filterArray = [[String:Any]]()
    var isFirstTime:Bool = true
    var productArray = [JSON]()
    var jsonToproductListing = [String:Any]()
    var homeArray = [String : JSON]()
    var recentBool = Bool()
    var categoryBool = Bool()
    var txtIsAutoFillBool = Bool()
    var requiredJson: [String: Any] = [:]
    var categoryNameArray = [String]()
    // MARK: - View lifecycle
    // MARK: -
    
    override func viewDidLoad() {
        super.viewDidLoad()
        txtSearch.delegate = self
      
    }
    override func viewWillAppear(_ animated: Bool) {
        
        let defaults = UserDefaults.standard
        if defaults.value(forKey: "homeCategoryName") != nil {
            categoryNameArray = defaults.array(forKey: "homeCategoryName")  as? [String] ?? [String]()
            if categoryNameArray.count == 0 {
               ApiCallToGetHomeData()
            } else {
                self.collectionView.dataSource = self
                self.collectionView.delegate = self
                collectionView.reloadData()
            }
        } else {
            ApiCallToGetHomeData()
        }
        UserDefaults.standard.removeObject(forKey: "category_Array")
        UserDefaults.standard.removeObject(forKey: "brand_Array")
        UserDefaults.standard.synchronize()
        self.navigationController?.setNavigationBarHidden(true, animated: true)
        recentArr = UserDefaults.standard.stringArray(forKey: "recent_search") ?? [String]()
        if recentArr.count != 0 {
            let tags = recentArr.map{self.button(with: $0 )}
            for (i,btn) in tags.enumerated()
            {
                btn.tag = i
                btn.addTarget(self, action: #selector(btnRecentAction), for: .touchUpInside)
            }
            self.tagViewHeight.constant = CGFloat(self.tagView.create(cloud: tags, inView: self.tagView))
            viewRecent.isHidden = false
            viewRecentHeight.constant = 30
        }
        else {
            viewRecent.isHidden = true
            viewRecentHeight.constant = 0
        }
    }
    
    // MARK: - Button Actions
    // MARK: -
    
    @objc func btnRecentAction(sender: UIButton){
        txtIsAutoFillBool = true
        self.txtSearch.text = ""
        print(sender.tag)
        self.txtSearch.text = recentArr[sender.tag]
        mustArray.removeAll()
        let mustQueryDict = ["query_string":["query": txtSearch.text!]]
        let isVisibleDict = ["match" :["visibility_id":["query": "Catalog Search", "operator": "and"]]]
        mustArray.append(mustQueryDict)
        mustArray.append(isVisibleDict)
        ApiCallForElasticSearch()
        isFirstTime = false
    }
    @objc func btncategoryAction(sender: UIButton) {
        txtIsAutoFillBool = true
        self.txtSearch.text = ""
        self.txtSearch.text = categoryNameArray[sender.tag]
        mustArray.removeAll()
        let mustQueryDict = ["query_string":["query": txtSearch.text]]
        let isVisibleDict = ["match" :["visibility_id":["query": "Catalog Search", "operator": "and"]]]
        mustArray.append(mustQueryDict)
        mustArray.append(isVisibleDict)
        ApiCallForElasticSearch()
        filterArray.removeAll()
        isFirstTime = true
    }
    
    @IBAction func btnBackTappef(_ sender: Any) {
        self.navigationController?.popViewController(animated: true)
    }
    //    MARK:- Voice Recoginsation
    @IBAction func btnVoiceSearchAction(_ sender: Any) {
        
        let vc = storyboard?.instantiateViewController(withIdentifier: "SpeechViewController") as! SpeechViewController
        vc.delegate = self
        self.navigationController?.pushViewController(vc, animated: true)
    }
    private func button(with title: String) -> UIButton {
        let font = UIFont(name: "hind-medium", size: 16)
        let attributes: [NSAttributedString.Key: Any] = [.font: font!]
        let button = UIButton(type: .custom)
        button.titleLabel?.font = font
        let size = title.size(withAttributes: attributes)
        button.backgroundColor = .white
        button.layer.cornerRadius = 5
        button.layer.borderColor = UIColor.lightGray.cgColor
        button.layer.borderWidth = 1.0
        button.setTitleColor(.black, for: .normal)
        button.setTitle(title, for: .normal)
        button.frame = CGRect(x: 0.0, y: 0.0, width: size.width + 32.0, height: size.height + 10.0)
        button.titleEdgeInsets = UIEdgeInsets(top: 0.0, left: 16.0, bottom: 0.0, right: 16.0)
        return button
    }
    // MARK: - Audio Function
    // MARK: -
    
    func MicTypeSelected(text: String) {
        self.requiredJson = [:]
        self.txtSearch.text = text
        self.productArray.removeAll()
        tableView.reloadData()
        mustArray.removeAll()
        let mustQueryDict = ["query_string":["query": text]]
        let isVisibleDict = ["match" :["visibility_id":["query": "Catalog Search", "operator": "and"]]]
        mustArray.append(mustQueryDict)
        mustArray.append(isVisibleDict)
        ApiCallForElasticSearch()
        isFirstTime = false
    }
    
    // MARK: - Search Method
    func textFieldShouldReturn(_ textField: UITextField) -> Bool
    {
        if txtSearch.text!.trimmingCharacters(in: .whitespaces).isEmpty == false  {
            if recentArr.contains(txtSearch.text!)  {
            }
            else {
                if recentArr.count > 10 {
                    recentArr.remove(at: 0)
                   recentArr.append(txtSearch.text!)
                }
                else {
                    
                       recentArr.append(txtSearch.text!)
                    
                }
            }
            txtSearch.resignFirstResponder()
            UserDefaults.standard.set(recentArr, forKey: "recent_search")
            UserDefaults.standard.synchronize()
            let enterSearchString = txtSearch.text!
            print(enterSearchString.count)
            if enterSearchString.count > 2 {
                if self.productArray.count != 0 {
                     NavigateToProductListingFromSearch()
                }
                
            }
        }
        return true
    }
    func textField(_ textField: UITextField, shouldChangeCharactersIn range: NSRange, replacementString string: String) -> Bool {
        if let text:NSString = txtSearch.text as NSString? {
            let txtAfterUpdate = text.replacingCharacters(in: range, with: string)
            if txtAfterUpdate.count > 1 {
                if txtIsAutoFillBool != true {
                    mustArray.removeAll()
                    let mustQueryDict = ["query_string":["query": txtAfterUpdate]]
                    let isVisibleDict = ["match" :["visibility_id":["query": "Catalog Search", "operator": "and"]]]
                    mustArray.append(mustQueryDict)
                    mustArray.append(isVisibleDict)
                    ApiCallForElasticSearch()
                    isFirstTime = false
                    viewWillAppear(true)
                }
            }
        }
        return true
    }
    func estimatedFrame(text: String, font: UIFont) -> CGRect {
        let size = CGSize(width: 200, height: 1000) // temporary size
        let options = NSStringDrawingOptions.usesFontLeading.union(.usesLineFragmentOrigin)
        return NSString(string: text).boundingRect(with: size, options: options, attributes: [NSAttributedString.Key.font: font], context: nil)
    }
    
    func NavigateToProductListingFromSearch() {
        let storyboard: UIStoryboard = UIStoryboard(name: "Home", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "ProductListingViewController") as! ProductListingViewController
        let jsonData = try! JSONSerialization.data(withJSONObject: jsonToproductListing)
        let jsonString = String(data: jsonData, encoding: .utf8)
        print(jsonString ?? "Wrong data")
        vc.jsonFromSearch = jsonToproductListing
        vc.isFirstTimefromSearch = true
        vc.isFirstTime = false
        vc.mustArrayFromSearch = mustArray
        vc.filterArrayFromSearch = filterArray
        
        if txtSearch.text!.trimmingCharacters(in: .whitespaces).isEmpty == false  {
            if recentArr.contains(txtSearch.text!)  {
            }
            else {
                if recentArr.count > 10 {
                    recentArr.remove(at: recentArr.count-1)
                   recentArr.append(txtSearch.text!)
                }
                else {
                   recentArr.append(txtSearch.text!)
                }
            }
            txtSearch.resignFirstResponder()
            UserDefaults.standard.set(recentArr, forKey: "recent_search")
            UserDefaults.standard.synchronize()
            let enterSearchString = txtSearch.text!
            print(enterSearchString.count)
            if enterSearchString.count > 2 {
                if self.productArray.count != 0 {
                    self.navigationController?.pushViewController(vc, animated: true)
                }
            }
        }
       // self.navigationController?.pushViewController(vc, animated: true)
    }
    // MARK: - Api Calling
    // MARK: -
    func ApiCallForElasticSearch()
    {
        if isFirstTime {
            let filterFirst = ["nested": ["path": "inventory" , "score_mode": "avg", "query": ["bool" :["must": [["term" :["inventory.id" : wareHouseId] ],["range" : ["inventory.stock" : ["gt" : 0]]]]]]] ]
            
            let filterSecond = ["nested" : ["path": "channel_currency_product_price" , "query": [["bool":["must": [["range": ["channel_currency_product_price.new_default_price" : ["gt":0]]],["term":["channel_currency_product_price.warehouse_id" : wareHouseId]]]]]]]]
            
            let filterThird  = ["nested": ["path": "product_images","query":["bool":["must":[["term" : ["product_images.is_cover":1]]]]]]]
            filterArray.append(filterFirst)
            filterArray.append(filterSecond)
            filterArray.append(filterThird)
        }
        
         requiredJson = ["table_name":"EngageboostProducts" , "website_id" : "1", "data" : ["query": ["bool" :["must" : mustArray, "filter" : filterArray]], "from": 0 ,"size": 100 ] ]// Demo
      //  requiredJson = ["query": ["bool" :["must" : mustArray, "filter" : filterArray]], "from": 0 ,"size": 100]
        jsonToproductListing = requiredJson
        print(requiredJson)
        let jsonData = try! JSONSerialization.data(withJSONObject: requiredJson)
        let jsonString = String(data: jsonData, encoding: .utf8)
        print(jsonString ?? "Wrong data")
        postMethodQuery1(apiName: searchElasticApiLive, params: requiredJson, vc: self) { (response : JSON) in
            let testSearchArray = response["hits"]["hits"].arrayValue
            if testSearchArray.count != 0 {
                self.productArray = testSearchArray
                self.tableView.dataSource = self
                self.tableView.delegate = self
                self.tableView.reloadData()
                self.noProductView.isHidden = true
            }
            else {
                self.productArray.removeAll()
                self.tableView.delegate = self
                self.tableView.dataSource = self
                self.tableView.reloadData()
                self.noProductView.isHidden = false
            }
            
        }
    }
    func ApiCallToGetHomeData() {
        var params = [String:Any]()
        params["company_website_id"] = 1
        params["lang"] = "en"
        params["template_id"] = 1
        params["page_id"] = 9
        params["start_limit"] = 0
        params["end_limit"] = 70
        params["warehouse_id"] = wareHouseId
        postMethodSocialSignIn(apiName: "home-cms/", params: params, vc: self) { (response:JSON) in
            if response["status"].stringValue == "200" {
                self.homeArray = response["data"].dictionaryValue
                let dataDict = response["data"].dictionaryValue
                if dataDict["Shop_By_Category"]?.arrayValue.count != 0 {
                    let cArray = dataDict["Shop_By_Category"]?.arrayValue
                    for index in cArray! {
                        if index["image"].string!.isEmpty != true {
                            self.categoryNameArray.append(index["name"].string ?? "")
                        }
                    }
                    self.collectionView.dataSource = self
                    self.collectionView.delegate = self
                    self.collectionView.reloadData()
                }
            }
        }
    }
    //MARK:- Events
    //MARK:-
    func SearchProduct(dictParam : [String:Any]) {
        Analytics.logEvent("search_product", parameters:  dictParam)
    }
}
// MARK: - External Class
// MARK: -

class TagsView: UIView {
    var offset: CGFloat = 5
    func create(cloud tags: [UIButton], inView:TagsView) -> Float {
        var x = offset
        var y = offset
        var totalHeight:Float = 0
        let screenSize = inView.bounds
        let screenWidth = screenSize.width
        for (index, tag) in tags.enumerated() {
            tag.frame = CGRect(x: x, y: y, width: tag.frame.width, height: tag.frame.height)
            x += tag.frame.width + offset
            let nextTag = index <= tags.count - 2 ? tags[index + 1] : tags[index]
            let nextTagWidth = nextTag.frame.width + offset
            if x + nextTagWidth > screenWidth {
                x = offset
                y += tag.frame.height + offset
                totalHeight = Float(y) + Float(offset)
            }
            else
            {
                totalHeight = Float(y) + Float(tag.frame.height + offset)
            }
            inView.addSubview(tag)
        }
        return totalHeight
    }
}

extension SearchViewController : UITableViewDelegate , UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return self.productArray.count
    }
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "SearchDisplayTableViewCell", for: indexPath) as! SearchDisplayTableViewCell
        let productDict = productArray[indexPath.row].dictionaryValue
        print(productDict)
        let sourceDict = productDict["_source"]?.dictionaryValue
        let productImagesArray = sourceDict!["product_images"]?.arrayValue
        let imageDict = productImagesArray![0].dictionaryValue
        let url = imageDict["link"]?.stringValue
        if let brandurl = imageDict["img"]?.stringValue{
            let fullUrl = url! + brandurl
            let url = URL(string: fullUrl)
            cell.imgImage.sd_setImage(with: url!)
        }
        let priceArr = sourceDict!["channel_currency_product_price"]!.arrayValue
        for index in priceArr {
            if index["warehouse_id"].intValue == self.wareHouseId && index["price_type"].intValue == 1 {
                cell.lblPrice.text = "AED \(index["new_default_price_unit"].doubleValue)"
            }
        }
        cell.lblTitle.text = sourceDict!["name"]?.stringValue
        return cell
    }
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        let productDict = productArray[indexPath.row].dictionaryValue
        let sourceDict = productDict["_source"]!.dictionaryValue
        let slug = sourceDict["slug"]!.stringValue
        let vc = self.storyboard?.instantiateViewController(withIdentifier: "ProductDetailViewController") as! ProductDetailViewController
        vc.slugInDetail = slug
        
        let contentName = sourceDict["name"]?.stringValue
        let productId = productDict["_id"]!.intValue
        let priceArr = sourceDict["channel_currency_product_price"]!.arrayValue
        var cost = String()
        for index in priceArr {
            if index["warehouse_id"].intValue == self.wareHouseId && index["price_type"].intValue == 1 {
                cost = "\(index["new_default_price_unit"].doubleValue)"
            }
        }
        let dictParam :[String:Any] = ["Content_ID":"\(productId)","Content_Type":contentName!,"Currency":"AED","ValueToSum":cost]
        print(dictParam)
        self.SearchProduct(dictParam: dictParam)
        logSearchEvent(content_ID: "\(productId)", content_Type: contentName!, currency: "AED", valueToSum: cost)
        self.navigationController?.pushViewController(vc, animated: true)
    }
    
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        return 100.0
    }
}
extension SearchViewController : UICollectionViewDelegate , UICollectionViewDataSource ,UICollectionViewDelegateFlowLayout{
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        return categoryNameArray.count
    }
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell1 = collectionView.dequeueReusableCell(withReuseIdentifier: "SearchCollectionViewCell", for: indexPath) as! SearchCollectionViewCell
        cell1.btnSuggested.setTitle(categoryNameArray[indexPath.row], for: .normal)
        cell1.btnSuggested.layer.cornerRadius = cell1.btnSuggested.frame.height/2
        cell1.btnSuggested.clipsToBounds = true
        cell1.btnSuggested.layer.borderColor  = UIColor.lightGray.cgColor
        cell1.btnSuggested.layer.borderWidth = 1.0
        cell1.btnSuggested.tag = indexPath.row
        cell1.btnSuggested.addTarget(self, action: #selector(btncategoryAction), for: .touchUpInside)
        return cell1
    }
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        self.txtSearch.text = ""
        self.txtSearch.text = categoryNameArray[indexPath.row]
        mustArray.removeAll()
        let mustQueryDict = ["query_string":["query": txtSearch.text]]
        let isVisibleDict = ["match" :["visibility_id":["query": "Catalog Search", "operator": "and"]]]
        mustArray.append(mustQueryDict)
        mustArray.append(isVisibleDict)
        ApiCallForElasticSearch()
        isFirstTime = false
        
    }
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, sizeForItemAt indexPath: IndexPath) -> CGSize {
        let cell1 = collectionView.dequeueReusableCell(withReuseIdentifier: "SearchCollectionViewCell", for: indexPath) as! SearchCollectionViewCell
        let title = categoryNameArray[indexPath.row]
        let font = UIFont(name: "hind-medium", size: 16)
        let attributes: [NSAttributedString.Key: Any] = [.font: font!]
        let size = title.size(withAttributes: attributes)
        cell1.btnSuggested.frame = CGRect(x: 0.0, y: 0.0, width: size.width + 32.0, height: size.height + 10.0)
        cell1.btnSuggested.titleEdgeInsets = UIEdgeInsets(top: 0.0, left: 16.0, bottom: 0.0, right: 16.0)
        return CGSize(width: cell1.btnSuggested.frame.width + 30, height: 35)
    }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, minimumInteritemSpacingForSectionAt section: Int) -> CGFloat {
        return 8
    }
}


