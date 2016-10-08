import time


class AllegroUser(object):
    """ WSDL API Allegro User
    Do not use it if only You can use SafeAllegroUser"""

    def __init__(self, api, user_id, session_id, start_time):
        self.api = api
        self.user_id = user_id
        self.session_id = session_id
        self.start_time = start_time

    def __repr__(self):
        return 'AllegroUser[' + str(self.user_id) + ']'

    # ######## My Allegro section ############

    def get_favourite_categories(self):
        return self.api.client.service.doGetFavouriteCategories(sessionHandle=self.session_id)

    def get_favourite_sellers(self):
        return self.api.client.service.doGetFavouriteSellers(sessionHandle=self.session_id)

    def get_bid_items(self, sort_by=None, sort_order=None,
                      filter_search=None, filter_category_id=None, filter_item_ids=None,
                      page_size=None, page_number=None):
        """
        :param sort_by: 1  - offer end time (default)   \n
                        2  - actual price               \n
                        3  - offer name                 \n
                        4  - number of buy offers       \n
                        5  - biggest bid                \n
                        6  - buyer login                \n
                        8  - my max price               \n
                        12 - amount of item
        :param sort_order: 1 - ascend (default)         \n
                           2 - descend
        :param filter_search:       search condition in title, you can use * - () ""
        :param filter_category_id:  only bid from this category
        :param filter_item_ids:     only for specified items (list)
        :param page_size:           amount of returned items (min=1, max=1000, default=100)
        :param page_number:         default 0
        """
        request = {'sessionId': self.session_id}
        if sort_by is not None or sort_order is not None:
            request['sortOptions'] = {}
            if sort_by is not None:
                request['sortOptions']['sortType'] = sort_by
            if sort_order is not None:
                request['sortOptions']['sortOrder'] = sort_order
        if filter_search is not None:
            request['searchValue'] = filter_search
        if filter_category_id is not None:
            request['categoryId'] = filter_category_id
        if filter_item_ids is not None:
            request['itemIds'] = filter_item_ids
        if page_size is not None:
            request['pageSize'] = page_size
        if page_number is not None:
            request['pageNumber'] = page_number
        return self.api.client.service.doGetMyBidItems(**request)

    def get_future_items(self, sort_by=None, sort_order=None,
                         filter_offer_type=None, filter_category_id=None, filter_item_ids=None,
                         page_size=None, page_number=None):
        """
        :param sort_by: 3  - offer name                     \n
                        13 - start date (default)
        :param sort_order:  1 - ascend (default)            \n
                            2 - descend
        :param filter_offer_type: 0 - all (default)         \n
                                  1 - only Allegro offers   \n
                                  2 - only shop offers
        :param filter_category_id: only offers from specified category
        :param filter_item_ids:    only offers for specified items (max 100 items)
        :param page_size:   amount of returned items (min=1, max=1000, default=100)
        :param page_number: default 0
        """
        request = {'sessionId': self.session_id}
        if sort_by is not None or sort_order is not None:
            request['sortOptions'] = {}
            if sort_by is not None:
                request['sortOptions']['sortType'] = sort_by
            if sort_order is not None:
                request['sortOptions']['sortOrder'] = sort_order
        if filter_offer_type is not None:
            request['filterOptions'] = {'filterFormat': filter_offer_type}
        if filter_category_id is not None:
            request['categoryId'] = filter_category_id
        if filter_item_ids is not None:
            request['itemIds'] = filter_item_ids
        if page_size is not None:
            request['pageSize'] = page_size
        if page_number is not None:
            request['pageNumber'] = page_number
        return self.api.client.service.doGetMyFutureItems(**request)

    def get_not_sold_items(self, sort_by=None, sort_order=None,
                           filter_offer_type=None, filter_end_date=None, filter_auto_renew=None, filter_price_from=None,
                           filter_price_to=None, filter_search=None, filter_category_id=None, filter_item_ids=None,
                           page_size=None, page_number=None):
        """
        :param sort_by: 1 - offer end time (default)        \n
                        2 - actual price                    \n
                        3 - offer name                      \n
                        4 - number of offers                \n
                        5 - highest offer                   \n
                        7 - minimum price                   \n
                        9 - amount offered
        :param sort_order:  1 - ascend                      \n
                            2 - descend (default)
        :param filter_offer_type: 0 - all (default)         \n
                                  1 - only Allegro offers   \n
                                  2 - only shop offers
        :param filter_end_date: 0  - show all (default)     \n
                                7  - two days past          \n
                                8  - three days past        \n
                                9  - four days past         \n
                                10 - five days past         \n
                                11 - six days past          \n
                                12 - seven days past
        :param filter_auto_renew: 0 - all offers (default)  \n
                                  1 - without auto renew    \n
                                  2 - with auto renew       \n
                                  3 - with auto renew and full amount
        :param filter_price_from:   minimum price
        :param filter_price_to:     maximum price
        :param filter_search:       search condition in title, you can use * - () ""
        :param filter_category_id:  only offers from specified category
        :param filter_item_ids:     only offers for specified items (max 100 items)
        :param page_size:           amount of returned items (min=1, max=1000, default=100)
        :param page_number:         default 0
        """
        request = {'sessionId': self.session_id}
        if sort_order is not None or sort_by is not None:
            request['sortOptions'] = {}
            if sort_by is not None:
                request['sortOptions']['sortType'] = sort_by
            if sort_order is not None:
                request['sortOptions']['sortOrder'] = sort_order
        filter_options = {filter_offer_type, filter_end_date, filter_auto_renew, filter_price_from, filter_price_to}
        if len(filter_options) > 1 or filter_options.pop() is not None:
            request['filterOptions'] = {}
            if filter_offer_type is not None:
                request['filterOptions']['filterFormat'] = filter_offer_type
            if filter_end_date is not None:
                request['filterOptions']['filterFromEnd'] = filter_end_date
            if filter_auto_renew is not None:
                request['filterOptions']['filterAutoListing'] = filter_auto_renew
            if filter_price_from is not None or filter_price_to is not None:
                request['filterOptions']['filterPrice'] = {}
                if filter_price_from is not None:
                    request['filterOptions']['filterPrice']['filterPriceFrom'] = filter_price_from
                if filter_price_to is not None:
                    request['filterOptions']['filterPrice']['filterPriceTo'] = filter_price_to
        if filter_search is not None:
            request['searchValue'] = filter_search
        if filter_category_id is not None:
            request['categoryId'] = filter_category_id
        if filter_item_ids is not None:
            request['itemIds'] = filter_item_ids
        if page_size is not None:
            request['pageSize'] = page_size
        if page_number is not None:
            request['pageNumber'] = page_number
        return self.api.client.service.doGetMyNotSoldItems(**request)

    def get_not_won_items(self, sort_by=None, sort_order=None,
                          filter_search=None, filter_category_id=None, filter_item_ids=None,
                          page_size=None, page_number=None):
        """
        :param sort_by: 1 - offer end time (default)        \n
                        2 - actual price                    \n
                        3 - offer name                      \n
                        4 - number of offers                \n
                        5 - highest offer                   \n
                        8 - my maximum offer
        :param sort_order:  1 - ascend                      \n
                            2 - descend (default)
        :param filter_search:       search condition in title, you can use * - () ""
        :param filter_category_id:  only offers from specified category
        :param filter_item_ids:     only offers for specified items (max 100 items)
        :param page_size:           amount of returned items (min=1, max=1000, default=100)
        :param page_number:         default 0
        """
        request = {'sessionId': self.session_id}
        if sort_order is not None or sort_by is not None:
            request['sortOptions'] = {}
            if sort_by is not None:
                request['sortOptions']['sortType'] = sort_by
            if sort_order is not None:
                request['sortOptions']['sortOrder'] = sort_order
        if filter_search is not None:
            request['searchValue'] = filter_search
        if filter_category_id is not None:
            request['categoryId'] = filter_category_id
        if filter_item_ids is not None:
            request['itemIds'] = filter_item_ids
        if page_size is not None:
            request['pageSize'] = page_size
        if page_number is not None:
            request['pageNumber'] = page_number
        return self.api.client.service.doGetMyNotWonItems(**request)

    def get_sell_items(self, sort_by=None, sort_order=None,
                       filter_offer_type=None, filter_bids=None, filter_to_end=None, filter_from_start=None,
                       filter_auto_renew=None, filter_price_from=None, filter_price_to=None, filter_search=None,
                       filter_category_id=None, filter_item_ids=None,
                       page_size=None, page_number=None):
        """
        :param sort_by: 1  - offer end time (default)       \n
                        2  - actual price                   \n
                        3  - offer name                     \n
                        4  - number of offers               \n
                        5  - highest offer                  \n
                        7  - minimum price                  \n
                        9  - amount offered                 \n
                        10 - amount sold items
        :param sort_order:  1 - ascend                      \n
                            2 - descend (default)
        :param filter_offer_type: 0 - all (default)         \n
                                  1 - only Allegro offers   \n
                                  2 - only shop offers
        :param filter_bids:     0 - all
                                1 - only with buy offer
                                2 - only without buy offer (default)
        :param filter_to_end:   0  - show all (default)     \n
                                2  - one hour               \n
                                3  - three hours            \n
                                4  - six hours              \n
                                5  - twelve hours           \n
                                6  - twenty four hours      \n
                                7  - two days               \n
                                8  - three days             \n
                                9  - four days              \n
                                10 - five days              \n
                                11 - six days               \n
                                12 - seven days
        :param filter_from_start:   0  - show all (default)     \n
                                    2  - one hour               \n
                                    3  - three hours            \n
                                    4  - six hours              \n
                                    5  - twelve hours           \n
                                    6  - twenty four hours      \n
                                    7  - two days               \n
                                    8  - three days             \n
                                    9  - four days              \n
                                    10 - five days              \n
                                    11 - six days               \n
                                    12 - seven days
        :param filter_auto_renew: 0 - all offers (default)  \n
                                  1 - without auto renew    \n
                                  2 - with auto renew       \n
                                  3 - with auto renew and full amount
        :param filter_price_from:   minimum price
        :param filter_price_to:     maximum price
        :param filter_search:       search condition in title, you can use * - () ""
        :param filter_category_id:  only offers from specified category
        :param filter_item_ids:     only offers for specified items (max 100 items)
        :param page_size:           amount of returned items (min=1, max=1000, default=100)
        :param page_number:         default 0
        """
        request = {'sessionId': self.session_id}
        if sort_order is not None or sort_by is not None:
            request['sortOptions'] = {}
            if sort_by is not None:
                request['sortOptions']['sortType'] = sort_by
            if sort_order is not None:
                request['sortOptions']['sortOrder'] = sort_order
        filter_options = {filter_offer_type, filter_bids, filter_to_end, filter_from_start,
                          filter_auto_renew, filter_price_from, filter_price_to}
        if len(filter_options) > 1 or filter_options.pop() is not None:
            request['filterOptions'] = {}
            if filter_offer_type is not None:
                request['filterOptions']['filterFormat'] = filter_offer_type
            if filter_bids is not None:
                request['filterOptions']['filterBids'] = filter_bids
            if filter_to_end is not None:
                request['filterOptions']['filterToEnd'] = filter_to_end
            if filter_from_start is not None:
                request['filterOptions']['filterFromStart'] = filter_from_start
            if filter_auto_renew is not None:
                request['filterOptions']['filterAutoListing'] = filter_auto_renew
            if filter_price_from is not None or filter_price_to is not None:
                request['filterOptions']['filterPrice'] = {}
                if filter_price_from is not None:
                    request['filterOptions']['filterPrice']['filterPriceFrom'] = filter_price_from
                if filter_price_to is not None:
                    request['filterOptions']['filterPrice']['filterPriceTo'] = filter_price_to
        if filter_search is not None:
            request['searchValue'] = filter_search
        if filter_category_id is not None:
            request['categoryId'] = filter_category_id
        if filter_item_ids is not None:
            request['itemIds'] = filter_item_ids
        if page_size is not None:
            request['pageSize'] = page_size
        if page_number is not None:
            request['pageNumber'] = page_number
        return self.api.client.service.doGetMySellItems(**request)

    def get_sold_items(self, sort_by=None, sort_order=None,
                       filter_offer_type=None, filter_from_end=None,
                       filter_auto_renew=None, filter_price_from=None, filter_price_to=None, filter_search=None,
                       filter_category_id=None, filter_item_ids=None,
                       page_size=None, page_number=None):
        """
        :param sort_by: 1  - offer end time (default)       \n
                        2  - actual price                   \n
                        3  - offer name                     \n
                        4  - number of offers               \n
                        5  - highest offer                  \n
                        7  - minimum price                  \n
                        9  - amount offered                 \n
                        10 - amount sold items
        :param sort_order:  1 - ascend                      \n
                            2 - descend (default)
        :param filter_offer_type: 0 - all (default)         \n
                                  1 - only Allegro offers   \n
                                  2 - only shop offers
        :param filter_from_end: 0  - show all (default)     \n
                                2  - one hour               \n
                                3  - three hours            \n
                                4  - six hours              \n
                                5  - twelve hours           \n
                                6  - twenty four hours      \n
                                7  - two days               \n
                                8  - three days             \n
                                9  - four days              \n
                                10 - five days              \n
                                11 - six days               \n
                                12 - seven days

        :param filter_auto_renew: 0 - all offers (default)  \n
                                  1 - without auto renew    \n
                                  2 - with auto renew       \n
                                  3 - with auto renew and full amount
        :param filter_price_from:   minimum price
        :param filter_price_to:     maximum price
        :param filter_search:       search condition in title, you can use * - () ""
        :param filter_category_id:  only offers from specified category
        :param filter_item_ids:     only offers for specified items (max 100 items)
        :param page_size:           amount of returned items (min=1, max=1000, default=100)
        :param page_number:         default 0
        """
        request = {'sessionId': self.session_id}
        if sort_order is not None or sort_by is not None:
            request['sortOptions'] = {}
            if sort_by is not None:
                request['sortOptions']['sortType'] = sort_by
            if sort_order is not None:
                request['sortOptions']['sortOrder'] = sort_order
        filter_options = {filter_offer_type, filter_from_end, filter_auto_renew, filter_price_from, filter_price_to}
        if len(filter_options) > 1 or filter_options.pop() is not None:
            request['filterOptions'] = {}
            if filter_offer_type is not None:
                request['filterOptions']['filterFormat'] = filter_offer_type
            if filter_from_end is not None:
                request['filterOptions']['filterFromEnd'] = filter_from_end
            if filter_auto_renew is not None:
                request['filterOptions']['filterAutoListing'] = filter_auto_renew
            if filter_price_from is not None or filter_price_to is not None:
                request['filterOptions']['filterPrice'] = {}
                if filter_price_from is not None:
                    request['filterOptions']['filterPrice']['filterPriceFrom'] = filter_price_from
                if filter_price_to is not None:
                    request['filterOptions']['filterPrice']['filterPriceTo'] = filter_price_to
        if filter_search is not None:
            request['searchValue'] = filter_search
        if filter_category_id is not None:
            request['categoryId'] = filter_category_id
        if filter_item_ids is not None:
            request['itemIds'] = filter_item_ids
        if page_size is not None:
            request['pageSize'] = page_size
        if page_number is not None:
            request['pageNumber'] = page_number
        return self.api.client.service.doGetMySoldItems(**request)

    def get_watched_items(self, sort_by=None, sort_order=None,
                          filter_search=None, filter_category_id=None, filter_item_ids=None,
                          page_size=None, page_number=None):
        """
        :param sort_by: 1 - offer end time (default)    \n
                        2 - actual price                \n
                        3 - offer name                  \n
                        4 - amount of buy offer         \n
                        5 - highest buy offer           \n
                        6 - seller login
        :param sort_order:  1 - ascend                  \n
                            2 - descend (default)
        :param filter_search:       search condition in title, you can use * - () ""
        :param filter_category_id:  only offers from specified category
        :param filter_item_ids:     only offers for specified items (max 100 items)
        :param page_size:           amount of returned items (min=1, max=1000, default=100)
        :param page_number:         default 0
        """
        request = {'sessionId': self.session_id}
        if sort_order is not None or sort_by is not None:
            request['sortOptions'] = {}
            if sort_by is not None:
                request['sortOptions']['sortType'] = sort_by
            if sort_order is not None:
                request['sortOptions']['sortOrder'] = sort_order
        if filter_search is not None:
            request['searchValue'] = filter_search
        if filter_category_id is not None:
            request['categoryId'] = filter_category_id
        if filter_item_ids is not None:
            request['itemIds'] = filter_item_ids
        if page_size is not None:
            request['pageSize'] = page_size
        if page_number is not None:
            request['pageNumber'] = page_number
        return self.api.client.service.doGetMyWatchedItems(**request)

    def get_watch_items(self, sort_by=None, sort_order=None,
                        filter_search=None, filter_category_id=None, filter_item_ids=None,
                        page_size=None, page_number=None):
        """
        :param sort_by: 1 - offer end time (default)    \n
                        2 - actual price                \n
                        3 - offer name                  \n
                        4 - amount of buy offer         \n
                        5 - highest buy offer           \n
                        6 - seller login
        :param sort_order:  1 - ascend  (default)       \n
                            2 - descend
        :param filter_search:       search condition in title, you can use * - () ""
        :param filter_category_id:  only offers from specified category
        :param filter_item_ids:     only offers for specified items (max 100 items)
        :param page_size:           amount of returned items (min=1, max=1000, default=100)
        :param page_number:         default 0
        """
        request = {'sessionId': self.session_id}
        if sort_order is not None or sort_by is not None:
            request['sortOptions'] = {}
            if sort_by is not None:
                request['sortOptions']['sortType'] = sort_by
            if sort_order is not None:
                request['sortOptions']['sortOrder'] = sort_order
        if filter_search is not None:
            request['searchValue'] = filter_search
        if filter_category_id is not None:
            request['categoryId'] = filter_category_id
        if filter_item_ids is not None:
            request['itemIds'] = filter_item_ids
        if page_size is not None:
            request['pageSize'] = page_size
        if page_number is not None:
            request['pageNumber'] = page_number
        return self.api.client.service.doGetMyWatchItems(**request)

    def get_won_items(self, sort_by=None, sort_order=None,
                      filter_search=None, filter_category_id=None, filter_item_ids=None,
                      page_size=None, page_number=None):
        """
        :param sort_by: 1  - offer end time (default)    \n
                        2  - actual price                \n
                        3  - offer name                  \n
                        6  - seller login                \n
                        11 - amount of bought item       \n
        :param sort_order:  1 - ascend                   \n
                            2 - descend (default)
        :param filter_search:       search condition in title, you can use * - () ""
        :param filter_category_id:  only offers from specified category
        :param filter_item_ids:     only offers for specified items (max 100 items)
        :param page_size:           amount of returned items (min=1, max=1000, default=100)
        :param page_number:         default 0
        """
        request = {'sessionId': self.session_id}
        if sort_order is not None or sort_by is not None:
            request['sortOptions'] = {}
            if sort_by is not None:
                request['sortOptions']['sortType'] = sort_by
            if sort_order is not None:
                request['sortOptions']['sortOrder'] = sort_order
        if filter_search is not None:
            request['searchValue'] = filter_search
        if filter_category_id is not None:
            request['categoryId'] = filter_category_id
        if filter_item_ids is not None:
            request['itemIds'] = filter_item_ids
        if page_size is not None:
            request['pageSize'] = page_size
        if page_number is not None:
            request['pageNumber'] = page_number
        return self.api.client.service.doGetMyWonItems(**request)

    def my_account_data(self, filter_type=None, filter_item_ids=None, offset=None, limit=None):
        """
        :param filter_type: from which tab download data
                            bid      - already bidding items    \n
                            won      - bought items             \n
                            not_won  - not bought items         \n
                            watch    - already watched items    \n
                            watch_cl - watched ended items      \n
                            sell     - already selling items    \n
                            sold     - sold items               \n
                            not_sold - not sold items           \n
                            future   - scheduled items          \n
        :param filter_item_ids: only offers for specified items (probably max 100 or 25 items)
        :param offset: from which item start listing (default 0) index form 0,
                       items always sorted by end time ascend
        :param limit: how many items display (min=1, max=100, default=25)
        """
        request = {'sessionId': self.session_id}
        if filter_type is not None:
            request['accountType'] = filter_type
        if filter_item_ids is not None:
            request['itemsArray'] = filter_item_ids
        if offset is not None:
            request['offset'] = offset
        if limit is not None:
            request['limit'] = limit
        return self.api.client.service.doMyAccount2(**request)

    def get_items_count(self, filter_type=None, filter_item_ids=None):
        """
        :param filter_type: from which tab download data
                            bid      - already bidding items    \n
                            won      - bought items             \n
                            not_won  - not bought items         \n
                            watch    - already watched items    \n
                            watch_cl - watched ended items      \n
                            sell     - already selling items    \n
                            sold     - sold items               \n
                            not_sold - not sold items           \n
                            future   - scheduled items          \n
        :param filter_item_ids: only offers for specified items (probably max 100 or 25 items)
        """
        request = {'sessionId': self.session_id}
        if filter_type is not None:
            request['accountType'] = filter_type
        if filter_item_ids is not None:
            request['itemsArray'] = filter_item_ids
        return self.api.client.service.doMyAccountItemsCount(**request)

    def remove_watch(self, item_ids):
        """
        :param item_ids: item ids list or id to remove watch (max 25 items)
        """
        if isinstance(item_ids, int):
            item_ids = [item_ids]
        request = {'sessionId': self.session_id, 'itemsIdArray': item_ids}
        return self.api.client.service.doRemoveFromWatchList(**request)

    def get_profile(self):
        request = {'sessionHandle': self.session_id}
        return self.api.client.service.doGetMyData(**request)

    # ######## END My Allegro section ############
    # ####### LICENCE #######
    def give_licence_to_user(self, user_login, licence_date):
        """
        :param user_login:   user to give licence
        :param licence_date: date in timestamp format
        """
        request = {'adminSessionHandle': self.session_id, 'userLicLogin': user_login,
                   'userLicCountry': self.api.country_code, 'userLicDate': licence_date}
        return self.api.client.service.doSetUserLicenceDate(**request)

    # ####### END LICENCE #######


class SafeAllegroUser(AllegroUser):
    """REST API + WSDL API Allegro User (logged in using OAuth2)"""

    def __init__(self, api, user_id, session_id, start_time, access_token, refresh_token, valid_time):
        """This method should be called only by AllegroApi object"""
        super().__init__(api, user_id, session_id, start_time)
        self.end_time = self.start_time + valid_time
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.time_before_refresh = 120  # feel free to modify this after object created
        self.refresh_times_left = 365

    def need_refresh(self):
        """Check if token become invalid"""
        return self.end_time - time.time() <= self.time_before_refresh

    def get_new_token(self, force=False):
        self.refresh_times_left -= 1
        if not force and not self.need_refresh() or self.refresh_times_left == 0:
            return
        else:
            # TODO: implement this method https://github.com/Behoston/pyllegro/issues/1
            pass

            # TODO: implement first REST API 'default' method https://github.com/Behoston/pyllegro/issues/2
