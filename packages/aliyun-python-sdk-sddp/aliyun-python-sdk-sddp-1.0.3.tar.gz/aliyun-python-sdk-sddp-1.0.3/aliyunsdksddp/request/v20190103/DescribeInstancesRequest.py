# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdksddp.endpoint import endpoint_data

class DescribeInstancesRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Sddp', '2019-01-03', 'DescribeInstances')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_ProductCode(self):
		return self.get_query_params().get('ProductCode')

	def set_ProductCode(self,ProductCode):
		self.add_query_param('ProductCode',ProductCode)

	def get_ProductId(self):
		return self.get_query_params().get('ProductId')

	def set_ProductId(self,ProductId):
		self.add_query_param('ProductId',ProductId)

	def get_RiskLevelId(self):
		return self.get_query_params().get('RiskLevelId')

	def set_RiskLevelId(self,RiskLevelId):
		self.add_query_param('RiskLevelId',RiskLevelId)

	def get_Source(self):
		return self.get_query_params().get('Source')

	def set_Source(self,Source):
		self.add_query_param('Source',Source)

	def get_StartTime(self):
		return self.get_query_params().get('StartTime')

	def set_StartTime(self,StartTime):
		self.add_query_param('StartTime',StartTime)

	def get_UserId(self):
		return self.get_query_params().get('UserId')

	def set_UserId(self,UserId):
		self.add_query_param('UserId',UserId)

	def get_NameAccurate(self):
		return self.get_query_params().get('NameAccurate')

	def set_NameAccurate(self,NameAccurate):
		self.add_query_param('NameAccurate',NameAccurate)

	def get_SensLevelName(self):
		return self.get_query_params().get('SensLevelName')

	def set_SensLevelName(self,SensLevelName):
		self.add_query_param('SensLevelName',SensLevelName)

	def get_LastFinishTimeStart(self):
		return self.get_query_params().get('LastFinishTimeStart')

	def set_LastFinishTimeStart(self,LastFinishTimeStart):
		self.add_query_param('LastFinishTimeStart',LastFinishTimeStart)

	def get_PageSize(self):
		return self.get_query_params().get('PageSize')

	def set_PageSize(self,PageSize):
		self.add_query_param('PageSize',PageSize)

	def get_CheckStatus(self):
		return self.get_query_params().get('CheckStatus')

	def set_CheckStatus(self,CheckStatus):
		self.add_query_param('CheckStatus',CheckStatus)

	def get_Lang(self):
		return self.get_query_params().get('Lang')

	def set_Lang(self,Lang):
		self.add_query_param('Lang',Lang)

	def get_ServiceRegionId(self):
		return self.get_query_params().get('ServiceRegionId')

	def set_ServiceRegionId(self,ServiceRegionId):
		self.add_query_param('ServiceRegionId',ServiceRegionId)

	def get_FeatureType(self):
		return self.get_query_params().get('FeatureType')

	def set_FeatureType(self,FeatureType):
		self.add_query_param('FeatureType',FeatureType)

	def get_UserType(self):
		return self.get_query_params().get('UserType')

	def set_UserType(self,UserType):
		self.add_query_param('UserType',UserType)

	def get_EndTime(self):
		return self.get_query_params().get('EndTime')

	def set_EndTime(self,EndTime):
		self.add_query_param('EndTime',EndTime)

	def get_CurrentPage(self):
		return self.get_query_params().get('CurrentPage')

	def set_CurrentPage(self,CurrentPage):
		self.add_query_param('CurrentPage',CurrentPage)

	def get_Name(self):
		return self.get_query_params().get('Name')

	def set_Name(self,Name):
		self.add_query_param('Name',Name)

	def get_RuleId(self):
		return self.get_query_params().get('RuleId')

	def set_RuleId(self,RuleId):
		self.add_query_param('RuleId',RuleId)

	def get_LastFinishTimeEnd(self):
		return self.get_query_params().get('LastFinishTimeEnd')

	def set_LastFinishTimeEnd(self,LastFinishTimeEnd):
		self.add_query_param('LastFinishTimeEnd',LastFinishTimeEnd)