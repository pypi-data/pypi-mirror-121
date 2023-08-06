# -*- coding: utf-8 -*- 
# @Time : 9/29/21 9:31 AM 
# @Author : mxt
# @File : __init__.py.py
import gitlab
import logging
from typing import *
from pydantic import BaseModel

from .utils import *


class MergeRequestResponse(BaseModel):
    status: str = "0"
    message: str = ""
    navigateTo: str = ""


class GLObject:
    def __init__(self, url: str = "", private_token: str = ""):
        self.gl = gitlab.Gitlab(url=url, private_token=private_token)

    # 获取工程信息
    def get_project_info(self, project_id: Union[str, int], statistics: bool = False,
                         _license: bool = False, with_custom_attributes: bool = False):
        try:
            project = self.gl.projects.get(
                id=project_id,
                statistics=statistics,
                license=_license,
                with_custom_attributes=with_custom_attributes
            )
            return project.attributes
        except Exception as e:
            logging.getLogger(__name__).error("GLObject.get_project_info.error: %s" % str(e))
            return False

    # 创建组
    def create_groups(self, name: str = "", path: str = "", description: str = "", visibility: str = "private",
                      lfs_enabled: bool = False, request_access_enabled: bool = False):
        try:
            group = self.gl.groups.create({
                "name": name.upper(), "path": path, "description": description, "visibility": visibility,
                "lfs_enabled": lfs_enabled, "request_access_enabled": request_access_enabled
            })
            return group
        except Exception as e:
            logging.getLogger(__name__).error("GLObject.create_groups.error: %s" % str(e))
            return False

    # 创建分支
    def create_branch(self, project_id: Union[str, int], branch: str = "", ref: str = ""):
        try:
            project = self.gl.projects.get(project_id)
            _branch = project.branches.create({
                "branch": branch,
                "ref": ref
            })
            return _branch
        except Exception as e:
            logging.getLogger(__name__).error("GLObject.create_branch.error: %s" % str(e))
            return False

    # 删除分支
    def delete_branch(self, project_id: Union[str, int], branch: str = ""):
        try:
            project = self.gl.projects.get(project_id)
            project.branches.delete(branch)
        except Exception as e:
            logging.getLogger(__name__).error("GLObject.delete_branch.error: %s" % str(e))

    # 保护分支
    def protect_branch(self, project_id: Union[str, int], branch: str = "",
                       developers_can_push: bool = True, developers_can_merge: bool = True):
        try:
            project = self.gl.projects.get(project_id)
            _branch = project.branches.get(branch)
            _branch.protect(developers_can_push=developers_can_push, developers_can_merge=developers_can_merge)
        except Exception as e:
            logging.getLogger(__name__).error("GLObject.protect_branch.error: %s" % str(e))

    # 创建钩子
    def create_hook(self, project_id: Union[str, int], url: str = "", push_events: bool = True,
                    push_events_branch_filter: str = ""):
        try:
            project = self.gl.projects.get(project_id)
            hook = project.hook.create({
                "url": url,
                "push_events": push_events,
                "push_events_branch_filter": push_events_branch_filter
            })
            return hook
        except Exception as e:
            logging.getLogger(__name__).error("GLObject.create_hook.error: %s" % str(e))
            return False

    # 代码合并
    def merge_requests(self, project_id: Union[str, int], source_branch: str = "", target_branch: str = "",
                       title: str = "", description: str = ""):
        try:
            project = self.gl.projects.get(project_id)
            try:
                mr = project.mergerequests.create({
                    "source_branch": source_branch,
                    "target_branch": target_branch,
                    "title": title,
                    "description": description
                })
            except:
                mr = project.mergerequests.list(
                    source_branch=source_branch,
                    target_branch=target_branch,
                    state="opened"
                )[0]
            attr = mr.changes()
            commit_num = set(attr.get("diff_refs").values())
            name = attr.get("author").get("name")
            username = attr.get("author").get("username")
            created_at = get_time_diff(time_format(attr.get("created_at")))
            if attr.get("merge_status") == "can_be_merged":
                mr.merge()
                status = "0"
                navigete_to = ""
                message = u"由%s(%s)发起的合并请求：%s合并至%s，合并成功，正在触发流水线。" % (
                    name, username, source_branch, target_branch
                )
            else:
                status = "3" if len(commit_num) < 3 else "2"
                navigete_to = attr.get("web_url")
                message = u"%s由%s(%s)发起的合并请求：%s合并至%s请求失败，请处理后再次发起。" % (
                    created_at, name, username, source_branch, target_branch
                )
            return MergeRequestResponse(
                status=status, message=message, navigateTo=navigete_to
            )
        except Exception as e:
            logging.getLogger(__name__).error("GLObject.merge_requests.error: %s" % str(e))
            return False
