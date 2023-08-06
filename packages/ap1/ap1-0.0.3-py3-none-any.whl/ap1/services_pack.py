import traceback

class Services:
    def __init__(self,config,session,logger):
        self.config = config
        self.session = session
        self.logger = logger

    async def searchCompany(self,company_name):
        if 'search_company_api' not in self.config:
            raise Exception("Add search_company_api to config file")

        try:
            params = {"keyword": company_name}
            async with self.session.get(self.config['search_company_api'],params=params,verify_ssl=False) as resp:
                if resp.status == 200:
                    data = (await resp.json())['data']
                    if not data:
                        not_fined_msg=f"Company was not found: {company_name}"
                        self.logger.warning(not_fined_msg)
                        return None

                    fined_msg = f"Company was found: {company_name}"
                    self.logger.info(fined_msg)
                    return data[0]

        except Exception as e:
            self.logger.warning(e,traceback.format_exc())